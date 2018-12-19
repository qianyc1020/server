# coding=utf-8
import traceback

import core.globalvar as gl
from protocol.base.game_base_pb2 import ReqUpdatePlayerOnline


def execute(userId, message, messageHandle):
    online = ReqUpdatePlayerOnline()
    online.ParseFromString(message.data)
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            seat = room.getWatchSeatByUserId(userId)
            if seat is not None and seat.online != online.state:
                seat.online = online.state
                if not online.state:
                    room.exit(userId, messageHandle)
                seat = room.getSeatByUserId(userId)
                if seat is not None:
                    seat.online = online.state
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
