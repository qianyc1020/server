# coding=utf-8
import traceback

import core.globalvar as gl
from game.hongbao.command.client import reconnection_cmd
from game.hongbao.command.game import join_match_room_cmd, create_match_room_cmd
from protocol.service.match_pb2 import ReqApplyEnterMatch


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    redis.lock("match")
    if redis.exists(str(userId) + "_room"):
        reconnection_cmd.execute(userId, message, messageHandle)
        redis.unlock("match")
        return
    reqApplyEnterMatch = ReqApplyEnterMatch()
    reqApplyEnterMatch.ParseFromString(message.data)
    try:
        if redis.exists("11_rooms"):
            rooms = redis.get("11_rooms")
        else:
            rooms = []
        join = False
        for r in rooms:
            if redis.exists("room_" + str(r)):
                redis.lock("lockroom_" + str(r))
                room = redis.getobj("room_" + str(r))
                if room.roomNo != reqApplyEnterMatch.reject and room.matchLevel == reqApplyEnterMatch.level and (
                        room.count == -1 or 0 < len(room.seatNos)):
                    join_match_room_cmd.execute(userId, message, messageHandle, room)
                    redis.unlock("lockroom_" + str(r))
                    join = True
                    break
                redis.unlock("lockroom_" + str(r))
        if not join:
            create_match_room_cmd.execute(userId, message, messageHandle)
    except:
        print traceback.print_exc()
    redis.unlock("match")
