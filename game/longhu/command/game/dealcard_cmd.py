# coding=utf-8
import time
import traceback

import grpc

from game.longhu.mode.game_status import GameStatus
from protocol.base.base_pb2 import EXECUTE_ACTION
from protocol.base.game_base_pb2 import RecExecuteAction
from protocol.game import zhipai_pb2_grpc
from protocol.game.zhipai_pb2 import ShuffleData


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.WAITING:
            shuffleData = ShuffleData()
            conn = grpc.insecure_channel('127.0.0.1:50011')
            client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
            shuffleResult = client.shuffle(shuffleData)
            cardlist = shuffleResult.cardlistList
            i = 0
            for p in room.positions:
                p.cards.append(cardlist[i])
                i += 1
            room.startDate = int(time.time())
        # if room.gameStatus == GameStatus.PLAYING:
        # # TODO gameOver
        # else:
        executeAction = RecExecuteAction()
        executeAction.actionType = 0
        messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, room)
        room.gameStatus = GameStatus.PLAYING
        # TODO 下注计时器
        room.historyActions.append(executeAction.SerializeToString())
        room.executeAsk(messageHandle, 0, 2)
        # TODO 唤醒发送下注计时器
    except:
        print traceback.print_exc()
