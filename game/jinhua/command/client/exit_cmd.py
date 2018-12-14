# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.jinhua_room import JinhuaRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), JinhuaRoom(), JinhuaRoom().object_to_dict)
            room.exit(userId, messageHandle)
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
