# coding=utf-8
import traceback

import core.globalvar as gl


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if userId in room.bankerList:
                room.bankerList.remove(userId)
                room.updateBankerList(messageHandle, 0)
            elif room.banker == userId:
                room.xaizhuang = True
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
