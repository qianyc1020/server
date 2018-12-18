# coding=utf-8
import traceback

import grpc

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from mode.base.update_currency import UpdateCurrency
from protocol.game import zhipai_pb2_grpc
from protocol.game.zhipai_pb2 import ShuffleData


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.PLAYING:
            shuffleData = ShuffleData()
            conn = grpc.insecure_channel('127.0.0.1:50001')
            client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
            shuffleResult = client.shuffle(shuffleData)
            update_currency = []
            for seat in room.seats:
                seat.initialCards = []
                seat.initialCards.extend(shuffleResult.cardlist[3 * seat.seatNo - 3:3 * seat.seatNo])
                seat.playScore = room.score
                seat.score -= int(0.5 * room.score)
                update_currency.append(UpdateCurrency(-int(0.5 * room.score), seat.userId, room.roomNo))

            if 0 != len(update_currency):
                gl.get_v("update_currency").putall(update_currency)
            room.deskScore = room.score * len(room.seats)
            room.minScore = room.score
            gl.get_v("serverlogger").logger.info("发牌完成")
    except:
        print traceback.print_exc()
