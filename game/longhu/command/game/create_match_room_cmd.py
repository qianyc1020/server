# coding=utf-8
import random
import traceback

import core.globalvar as gl
from data.database import data_account
from game.longhu.command.game import join_match_room_cmd, gamestart_cmd
from game.longhu.mode.longhu_room import LonghuRoom
from mode.game.match_info import MatchInfo
from protocol.service.match_pb2 import ReqApplyEnterMatch


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        return
    reqApplyEnterMatch = ReqApplyEnterMatch()
    reqApplyEnterMatch.ParseFromString(message.data)
    account = data_account.query_account_by_id(None, userId)
    match_infos = gl.get_v("match_info")
    for match_info in match_infos:
        m = MatchInfo()
        m.__dict__ = match_info
        if m.level == reqApplyEnterMatch.level:
            if m.inScore <= account.gold:
                room = LonghuRoom(0, m.playerNum, 0, m.level, m.baseScore, m.inScore, m.leaveScore)
                redis.lock("lock8_rooms")
                try:
                    if redis.exists("8_rooms"):
                        rooms = redis.get("8_rooms")
                    else:
                        rooms = []
                    roomNo = random.randint(100000, 999999)
                    while roomNo in rooms:
                        roomNo = random.randint(100000, 999999)
                    rooms.append(roomNo)
                    room.roomNo = roomNo
                    room.save(redis)
                    redis.set(str(roomNo) + "_gameId", 8)
                    redis.set("8_rooms", rooms)
                    redis.lock("lockroom_" + str(roomNo))
                    join_match_room_cmd.execute(userId, message, messageHandle, room)
                    gamestart_cmd.execute(room, messageHandle)
                    room.save(redis)
                    redis.unlock("lockroom_" + str(roomNo))
                except:
                    traceback.print_exc()
                redis.unlock("lock8_rooms")
                return
            break
