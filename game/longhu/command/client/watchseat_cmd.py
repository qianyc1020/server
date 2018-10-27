# coding=utf-8
from decimal import Decimal

import core.globalvar as gl
from game.longhu.mode.longhu_room import LonghuRoom
from protocol.base.base_pb2 import WATCH_LIST
from protocol.base.game_base_pb2 import RecUpdateGameUsers


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    recUpdateGameUsers = RecUpdateGameUsers()
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)
        for s in room.watchSeats:
            userInfo = recUpdateGameUsers.users.add()
            userInfo.account = s.account
            userInfo.playerId = s.userId
            userInfo.headUrl = s.head
            userInfo.createTime = s.createDate
            userInfo.ip = s.ip
            userInfo.online = s.online
            userInfo.nick = s.nickname
            userInfo.ready = s.ready
            userInfo.score = int((s.score - s.playScore).quantize(Decimal('0')))
            userInfo.sex = s.sex
            userInfo.totalCount = s.total_count
            userInfo.consumeVip = s.level
        messageHandle.send_to_gateway(WATCH_LIST, recUpdateGameUsers)
