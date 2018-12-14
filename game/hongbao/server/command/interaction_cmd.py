# coding=utf-8
import traceback

import core.globalvar as gl
from game.hongbao.mode.hongbao_room import HongbaoRoom
from protocol.base.base_pb2 import GAME_PLAYER_INTERACTION
from protocol.base.game_base_pb2 import ReqGamePlayerInteraction, RecGamePlayerInteraction


def execute(userId, message, messageHandle):
    reqGamePlayerInteraction = ReqGamePlayerInteraction()
    reqGamePlayerInteraction.ParseFromString(message.data)

    recGamePlayerInteraction = RecGamePlayerInteraction()
    recGamePlayerInteraction.playerId = userId
    recGamePlayerInteraction.interactionId = reqGamePlayerInteraction.interactionId
    recGamePlayerInteraction.targetId = reqGamePlayerInteraction.targetId
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            messageHandle.broadcast_watch_to_gateway(GAME_PLAYER_INTERACTION, recGamePlayerInteraction, room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
