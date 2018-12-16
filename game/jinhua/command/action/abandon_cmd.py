# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("看牌失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and not seat.end:
                room.abandon(messageHandle, seat)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
