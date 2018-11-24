# coding=utf-8
import random
import traceback

import core.globalvar as gl
from data.database import data_account
from game.jinhua.command.game import join_match_room_cmd
from game.jinhua.mode.jinhua_room import JinhuaRoom
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
    for match_info in match_infos:
        m = MatchInfo()
        m.__dict__ = match_info
        if m.level == reqApplyEnterMatch.level:
            if m.inScore <= account.gold:
                room = JinhuaRoom(0, m.playerNum, 3 if m.level > 20 else 1, m.level, m.baseScore, m.inScore,
                                  m.leaveScore, m.level <= 20)
                redis.lock("lock1_rooms", 5000)
                try:
                    if redis.exists("1_rooms"):
                        rooms = redis.get("1_rooms")
                    else:
                        rooms = []
                    roomNo = random.randint(100000, 999999)
                    while roomNo in rooms:
                        roomNo = random.randint(100000, 999999)
                    rooms.append(roomNo)
                    room.roomNo = roomNo
                    redis.setobj("room_" + str(roomNo), room)
                    redis.set(str(roomNo) + "_gameId", 1)
                    redis.set("1_rooms", rooms)
                    redis.lock("lockroom_" + str(roomNo), 5000)
                    join_match_room_cmd.execute(userId, message, messageHandle, room)
                    redis.unlock("lockroom_" + str(roomNo))
                except:
                    traceback.print_exc()
                redis.unlock("lock1_rooms")
                return
            else:
                recMatchGame = RecMatchGame()
                recMatchGame.allocId = 1
                recMatchGame.level = reqApplyEnterMatch.level
                recMatchGame.state = 1
                messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)
            break
