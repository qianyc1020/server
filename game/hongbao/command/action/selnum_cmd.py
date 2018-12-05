# coding=utf-8
import traceback

import core.globalvar as gl
from game.hongbao.mode.hongbao_room import HongbaoRoom
from protocol.game.hongbao_pb2 import BaiRenHongbaoScore


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            if not room.started and room.banker == userId:
                hongbaoScore = BaiRenHongbaoScore()
                hongbaoScore.ParseFromString(message)
                if 10 > hongbaoScore.score > -1:
                    room.bankerSelectNum(hongbaoScore.score, messageHandle)
                    room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
