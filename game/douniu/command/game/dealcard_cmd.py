# coding=utf-8
import traceback

import grpc

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from protocol.base.base_pb2 import EXECUTE_ACTION
from protocol.base.game_base_pb2 import RecExecuteAction
from protocol.game import zhipai_pb2_grpc
from protocol.game.douniu_pb2 import DouniuCardAction
from protocol.game.zhipai_pb2 import ShuffleData


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.WAITING:
            shuffleData = ShuffleData()
            conn = grpc.insecure_channel('127.0.0.1:50002')
            client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
            shuffleResult = client.shuffle(shuffleData)
            for seat in room.seats:
                seat.initialCards = []
                seat.initialCards.extend(shuffleResult.cardlist[5 * seat.seatNo - 5:5 * seat.seatNo])
            gl.get_v("serverlogger").logger.info("发牌完成")
        executeAction = RecExecuteAction()
        if room.gameStatus == GameStatus.PLAYING:
            for s in room.seats:
                dealCardAction = DouniuCardAction()
                if 0 != len(s.initialCards):
                    dealCardAction.cards.append(s.initialCards[4])
                else:
                    dealCardAction.cards.append(0)
                executeAction.data = dealCardAction.SerializeToString()
                messageHandle.send_to_gateway(EXECUTE_ACTION, executeAction, s.userId)
            room.gameStatus = GameStatus.OPENING
            room.executeAsk(messageHandle, 0, 3)
        else:
            for s in room.seats:
                dealCardAction = DouniuCardAction()
                if 0 != len(s.initialCards):
                    dealCardAction.cards.extend(s.initialCards[0:4])
                else:
                    dealCardAction.cards.extend([0, 0, 0, 0])
                executeAction.data = dealCardAction.SerializeToString()
                messageHandle.send_to_gateway(EXECUTE_ACTION, executeAction, s.userId)
            room.gameStatus = GameStatus.GRABING
            room.executeAsk(messageHandle, 0, 1)
        room.historyActions.append(executeAction.SerializeToString())
    except:
        print traceback.print_exc()
