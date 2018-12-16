# coding=utf-8
import traceback

import core.globalvar as gl
from protocol.game.wuziqi_pb2 import WuziqiCreateRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        amount = WuziqiCreateRoom()
        amount.ParseFromString(message.data)
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            room.score = amount.countDown
            room.executeAction(userId, 0, amount, messageHandle)
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
