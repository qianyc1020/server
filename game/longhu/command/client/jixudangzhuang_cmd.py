# coding=utf-8
import traceback

import core.globalvar as gl
from game.longhu.mode.longhu_room import LonghuRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)
            room.setXiazhuang = False
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))