# coding=utf-8
import traceback

import core.globalvar as gl
from game.longhu.mode.longhu_room import LonghuRoom
from protocol.base.base_pb2 import PLAYER_VOICE
from protocol.base.game_base_pb2 import ReqGpsInfo


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)

            s = room.getSeatByUserId(userId)
            if s is not None:
                reqGpsInfo = ReqGpsInfo()
                reqGpsInfo.ParseFromString(message.data)
                s.gpsInfo = reqGpsInfo.gpsInfo
                messageHandle.broadcast_watch_to_gateway(PLAYER_VOICE, room.gpsinfo(), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
