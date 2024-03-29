# coding=utf-8
import traceback

import core.globalvar as gl
from protocol.base.base_pb2 import PLAYER_VOICE
from protocol.base.game_base_pb2 import ReqPlayerVoice, RecPlayerVoice


def execute(userId, message, messageHandle):
    reqPlayerVoice = ReqPlayerVoice()
    reqPlayerVoice.ParseFromString(message.data)

    recPlayerVoice = RecPlayerVoice()
    recPlayerVoice.playerId = userId
    recPlayerVoice.voiceData = reqPlayerVoice.voiceData
    recPlayerVoice.channels = reqPlayerVoice.channels
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            messageHandle.broadcast_watch_to_gateway(PLAYER_VOICE, recPlayerVoice, room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
