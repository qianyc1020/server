# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.douniu_room import DouniuRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
            room.exit(userId, messageHandle)
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
