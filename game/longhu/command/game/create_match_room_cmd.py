# coding=utf-8
import random
import traceback

import core.globalvar as gl
from data.database import data_account
from game.longhu.command.game import join_match_room_cmd
from game.longhu.mode.longhu_room import LonghuRoom
from mode.game.match_info import MatchInfo
from protocol.base.base_pb2 import GAME_SVR_MATCH
from protocol.base.game_base_pb2 import RecMatchGame
from protocol.service.match_pb2 import ReqApplyEnterMatch


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        return
    reqApplyEnterMatch = ReqApplyEnterMatch()
    reqApplyEnterMatch.ParseFromString(message.data)
    account = data_account.query_account_by_id(None, userId)
    match_infos = gl.get_v("match_info")
    recMatchGame = RecMatchGame()
    recMatchGame.allocId = 8
    recMatchGame.level = reqApplyEnterMatch.level
    recMatchGame.state = 1
    for match_info in match_infos:
        m = MatchInfo()
        m.__dict__ = match_info
        if m.level == reqApplyEnterMatch.level:
            if m.inScore <= account.gold:
                room = LonghuRoom(0, m.playerNum, 0, m.level, m.baseScore, m.inScore, m.leaveScore)
                redis.lock("lock8_rooms", 5000)
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
                    redis.setobj("room_" + str(roomNo), room)
                    redis.set(str(roomNo) + "_gameId", 8)
                    redis.set("8_rooms", rooms)
                    redis.lock("lockroom_" + str(roomNo), 5000)
                    join_match_room_cmd.execute(userId, message, messageHandle, room)
                    redis.unlock("lockroom_" + str(roomNo))
                except:
                    traceback.print_exc()
                redis.unlock("lock8_rooms")
                return
            break
    messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)
