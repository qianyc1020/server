# coding=utf-8
import threading
import time
import traceback

import grpc

import core.globalvar as gl
from game.tuitongzi.command.game import gameover_cmd
from game.tuitongzi.handle.playscore_handle import PlayScoreHandle
from game.tuitongzi.mode.game_status import GameStatus
from game.tuitongzi.timeout import play_timeout, open_timeout
from game.tuitongzi.timeout.send_scores_timeout import SendScores
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
                with open('./conf/tuitongzicheat.t') as infile:
                    strs = infile.read()
                    str = strs.split(',')
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(str[0])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(str[1])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(str[2])
                    cheatData = shuffleData.cheatData.add()
                    cheatData.level = int(str[3])
            except:
                print traceback.print_exc()

            conn = grpc.insecure_channel('127.0.0.1:50013')
            client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
            if room.reDealCard or len(room.surplusCards) < 8:
                shuffleResult = client.shuffle(shuffleData)
                room.reDealCard = False
                room.dealedCards = []
                room.surplusCards = []
                room.surplusCards.extend(shuffleResult.cardlist)
            room.positions[0].cards.extend(room.surplusCards[0:2])
            room.positions[1].cards.extend(room.surplusCards[2:4])
            room.positions[2].cards.extend(room.surplusCards[4:6])
            room.positions[3].cards.extend(room.surplusCards[6:8])
            for i in range(0, 8):
                room.surplusCards.remove(room.surplusCards[0])
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
            dealCardAction.cards.append(room.positions[0].cards[0])
            dealCardAction.cards.append(room.positions[1].cards[0])
            dealCardAction.cards.append(room.positions[2].cards[0])
            dealCardAction.cards.append(room.positions[3].cards[0])
            dealCardAction.dealedCards.extend(room.dealedCards)
            dealCardAction.cardSize = len(room.surplusCards) + 8
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
