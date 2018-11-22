# coding=utf-8
import traceback

import core.globalvar as gl
from game.wuziqi.mode.wuziqi_room import WuziqiRoom
from protocol.game.wuziqi_pb2 import WuziqiCreateRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), WuziqiRoom(), WuziqiRoom().object_to_dict)
            amount = WuziqiCreateRoom()
            amount.ParseFromString(message.data)
            room.score = amount.countDown
            room.executeAction(userId, 0, amount, messageHandle)
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
