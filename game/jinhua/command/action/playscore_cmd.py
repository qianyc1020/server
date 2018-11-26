# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from game.jinhua.mode.jinhua_room import JinhuaRoom
from protocol.game.jinhua_pb2 import JinhuaBetScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), JinhuaRoom(), JinhuaRoom().object_to_dict)
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("下注失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and seat.seatNo == room.operationSeat and not seat.end:
                betScoreAction = JinhuaBetScoreAction()
                betScoreAction.ParseFromString(message)
                if betScoreAction.score > seat.score - seat.playScore:
                    gl.get_v("serverlogger").logger.info("当前分数不够，当前分数%d， 下注分数%d" % (seat.score, seat.playScore))
                    redis.unlock("lockroom_" + str(roomNo))
                    return
                if betScoreAction.score < (room.minScore * 2 if seat.lookCard else seat.lookCard):
                    gl.get_v("serverlogger").logger.info(
                        "下注，低于最低下注分，最低分%d，下注分%d" % (seat.minScore, betScoreAction.score))
                    redis.unlock("lockroom_" + str(roomNo))
                    return
                if betScoreAction.score > (10 * room.score if seat.lookCard else 5 * room.score):
                    gl.get_v("serverlogger").logger.info("超出最大下注限制")
                    redis.unlock("lockroom_" + str(roomNo))
                    return
                room.playScore(seat, betScoreAction, messageHandle)
                redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
