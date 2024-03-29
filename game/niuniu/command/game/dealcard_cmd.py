# coding=utf-8
import threading
import time
import traceback

import grpc

import core.globalvar as gl
from game.niuniu.command.game import gameover_cmd
from game.niuniu.handle.playscore_handle import PlayScoreHandle
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.timeout import play_timeout, open_timeout
from game.niuniu.timeout.send_scores_timeout import SendScores
from protocol.base.base_pb2 import EXECUTE_ACTION
from protocol.base.game_base_pb2 import RecExecuteAction
from protocol.game import zhipai_pb2_grpc
from protocol.game.bairen_pb2 import BaiRenDealCardAction
from protocol.game.zhipai_pb2 import ShuffleData
from utils.TestQueue import TestQueue


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.WAITING:
            shuffleData = ShuffleData()

            try:
                with open('./conf/niuniucheat') as infile:
                    cheatDatastrs = infile.read()
                    cheatDatas = cheatDatastrs.split(',')
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(cheatDatas[0])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(cheatDatas[1])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(cheatDatas[2])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(cheatDatas[3])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(cheatDatas[4])
            except:
                print traceback.print_exc()

            conn = grpc.insecure_channel('127.0.0.1:50014')
            client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
            shuffleResult = client.shuffle(shuffleData)
            room.reDealCard = False
            room.dealedCards = []
            room.surplusCards = []
            room.surplusCards.extend(shuffleResult.cardlist)
            room.positions[0].cards.extend(room.surplusCards[0:5])
            room.positions[1].cards.extend(room.surplusCards[5:10])
            room.positions[2].cards.extend(room.surplusCards[10:15])
            room.positions[3].cards.extend(room.surplusCards[15:20])
            room.positions[4].cards.extend(room.surplusCards[20:25])
            room.startDate = int(time.time())
        if room.gameStatus == GameStatus.PLAYING:
            if not room.openCard:
                room.executeAction(0, 5, None, messageHandle)
                room.opencard = True
            gameover_cmd.execute(room, messageHandle)
        else:
            executeAction = RecExecuteAction()
            executeAction.actionType = 0

            executeAction = RecExecuteAction()
            dealCardAction = BaiRenDealCardAction()
            executeAction.data = dealCardAction.SerializeToString()
            messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, room)

            room.gameStatus = GameStatus.PLAYING
            room.historyActions.append(executeAction.SerializeToString())
            room.executeAsk(messageHandle, 0, 2)
            threading.Thread(target=play_timeout.execute, args=(room.roomNo, messageHandle, room.gameCount,),
                             name='play_timeout').start()  # 线程对象.
            threading.Thread(target=open_timeout.execute, args=(room.roomNo, room.gameCount, messageHandle,),
                             name='open_timeout').start()  # 线程对象.
            gl.get_v("serverlogger").logger.info("开始下注")
            playHandle = PlayScoreHandle(str(room.roomNo), TestQueue(), messageHandle)
            gl.get_v("play-handle")[str(room.roomNo)] = playHandle
            threading.Thread(target=playHandle.execute, name='playthread').start()  # 线程对象.

            if gl.get_v(str(room.roomNo) + "sendthread") is None:
                e = SendScores(room.roomNo, messageHandle)
                threading.Thread(target=e.execute, name='sendthread').start()  # 线程对象.
                gl.set_v(str(room.roomNo) + "sendthread", e)
    except:
        print traceback.print_exc()
