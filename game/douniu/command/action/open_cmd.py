# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from protocol.game.douniu_pb2 import DouniuCardAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        openCardAction = DouniuCardAction()
        openCardAction.ParseFromString(message)
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameStatus != GameStatus.OPENING:
                gl.get_v("serverlogger").logger.info("开牌失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and not seat.openCard:
                seat.openCard = True
                openCardAction.cards.extend(seat.initialCards)
                room.executeAction(seat.userId, 3, openCardAction, messageHandle)
                room.checkOpen(messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
