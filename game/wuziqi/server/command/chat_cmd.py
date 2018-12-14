# coding=utf-8
import traceback

import core.globalvar as gl
from game.wuziqi.mode.wuziqi_room import WuziqiRoom
from protocol.base.base_pb2 import PLAYER_CHAT
from protocol.base.game_base_pb2 import ReqPlayerChat, RecPlayerChat


def execute(userId, message, messageHandle):
    reqPlayerChat = ReqPlayerChat()
    reqPlayerChat.ParseFromString(message.data)

    recPlayerChat = RecPlayerChat()
    recPlayerChat.playerId = userId
    recPlayerChat.msg = reqPlayerChat.msg
    recPlayerChat.type = reqPlayerChat.type
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), WuziqiRoom(), WuziqiRoom().object_to_dict)
            messageHandle.broadcast_seat_to_gateway(PLAYER_CHAT, recPlayerChat, room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
