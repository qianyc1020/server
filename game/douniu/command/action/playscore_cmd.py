# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from game.douniu.mode.douniu_room import DouniuRoom
from protocol.game.douniu_pb2 import DouniuScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("下注失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and -1 == seat.playScore and not seat.guanzhan and room.banker != userId:
                betScoreAction = DouniuScoreAction()
                betScoreAction.ParseFromString(message)
                playScore = betScoreAction.score
                if playScore < room.betType * room.score:
                    playScore = room.betType * room.score
                seat.playScore = playScore
                betScoreAction.score = playScore
                room.executeAction(userId, 2, betScoreAction, messageHandle)
                room.checkPlay(messageHandle)
                redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
