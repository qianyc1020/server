# coding=utf-8
import traceback

import core.globalvar as gl
from game.hongbao.mode.hongbao_room import HongbaoRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            if userId in room.bankerList:
                room.bankerList.remove(userId)
                room.updateBankerList(messageHandle, 0)
            elif room.banker == userId:
                room.xaizhuang = True
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
