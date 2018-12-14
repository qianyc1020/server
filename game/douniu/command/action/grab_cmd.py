# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from game.douniu.mode.douniu_room import DouniuRoom
from protocol.game.douniu_pb2 import DouniuScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
            if room.gameStatus != GameStatus.GRABING:
                gl.get_v("serverlogger").logger.info("抢庄失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and -1 == seat.grab and not seat.guanzhan:
                maxGrab = seat.score / 30 / room.betType / room.score
                if 0 == maxGrab:
                    maxGrab = 1
                grabAction = DouniuScoreAction()
                grabAction.ParseFromString(message)
                if maxGrab > grabAction.score:
                    maxGrab = grabAction.score
                seat.grab = maxGrab
                room.executeAction(userId, 1, grabAction, messageHandle)
                room.checkGrab(messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
