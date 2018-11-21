# coding=utf-8
import threading
import time
import traceback

import grpc

import core.globalvar as gl
from game.niuniu.command.game import gameover_cmd
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.timeout import play_timeout, send_scores_timeout, open_timeout
from game.niuniu.timeout.send_scores_timeout import SendScores
from protocol.base.base_pb2 import EXECUTE_ACTION
from protocol.base.game_base_pb2 import RecExecuteAction
from protocol.game import zhipai_pb2_grpc
from protocol.game.bairen_pb2 import BaiRenDealCardAction
from protocol.game.zhipai_pb2 import ShuffleData


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.WAITING:
            shuffleData = ShuffleData()
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
            t = threading.Thread(target=play_timeout.execute, args=(room.roomNo, messageHandle,),
                                 name='handle')  # 线程对象.
            t.start()

            t = threading.Thread(target=open_timeout.execute, args=(room.roomNo, room.gameCount, messageHandle,),
                                 name='handle')  # 线程对象.
            t.start()
            gl.get_v("serverlogger").logger.info("开始下注")

            if gl.get_v(str(room.roomNo) + "sendthread") is None:
                e = SendScores(room.roomNo, messageHandle)
                t = threading.Thread(target=e.execute, name='handle')  # 线程对象.
                t.start()
                gl.set_v(str(room.roomNo) + "sendthread", e)
    except:
        print traceback.print_exc()
