# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from protocol.game.douniu_pb2 import DouniuScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        betScoreAction = DouniuScoreAction()
        betScoreAction.ParseFromString(message)
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("下注失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and -1 == seat.playScore and not seat.guanzhan and room.banker != userId:
                playScore = betScoreAction.score
                if playScore < room.betType * room.score:
                    playScore = room.betType * room.score
                seat.playScore = playScore
                betScoreAction.score = playScore
                room.executeAction(userId, 2, betScoreAction, messageHandle)
                room.checkPlay(messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
