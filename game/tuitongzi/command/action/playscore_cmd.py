# coding=utf-8

import core.globalvar as gl
from mode.game.playscore import PlayScore
from protocol.game.bairen_pb2 import BaiRenBetScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    betScoreAction = BaiRenBetScoreAction()
    betScoreAction.ParseFromString(message)
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        gl.get_v("play-handle")[str(roomNo)].queue.put(PlayScore(userId, betScoreAction))
