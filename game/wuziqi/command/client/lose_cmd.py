# coding=utf-8
import traceback

import core.globalvar as gl
from game.wuziqi.command.game import gameover_cmd
from game.wuziqi.mode.game_status import GameStatus
from game.wuziqi.mode.wuziqi_room import WuziqiRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), WuziqiRoom(), WuziqiRoom().object_to_dict)
            if room.gameStatus == GameStatus.PLAYING and 0 < room.score:
                gameover_cmd.execute(room, messageHandle, userId)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
