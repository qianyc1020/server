# coding=utf-8
import traceback

import core.globalvar as gl
from protocol.game.hongbao_pb2 import BaiRenHongbaoScore


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        hongbaoScore = BaiRenHongbaoScore()
        hongbaoScore.ParseFromString(message)
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if not room.started and room.banker == userId:
                if 10 > hongbaoScore.score > -1:
                    room.bankerSelectNum(hongbaoScore.score, messageHandle)
                    room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
