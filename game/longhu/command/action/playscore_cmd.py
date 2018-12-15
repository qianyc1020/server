# coding=utf-8
import traceback

import core.globalvar as gl
from core import config
from game.longhu.mode.game_status import GameStatus
from game.longhu.mode.longhu_room import LonghuRoom
from protocol.game.bairen_pb2 import BaiRenBetScoreAction


def execute(userId, message, messageHandle):
    gl.get_v("serverlogger").logger.info("下注1")
    redis = gl.get_v("redis")
    betScoreAction = BaiRenBetScoreAction()
    betScoreAction.ParseFromString(message)
    pingReturn = float(config.get("longhu", "pingReturn"))
    pingRatio = float(config.get("longhu", "pingRatio"))
    gl.get_v("serverlogger").logger.info("下注2")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        gl.get_v("serverlogger").logger.info("下注3")
        try:
            room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)
            gl.get_v("serverlogger").logger.info("下注4")
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("下注失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            if userId == room.banker:
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getWatchSeatByUserId(userId)
            if seat is None:
                redis.unlock("lockroom_" + str(roomNo))
                return
            gl.get_v("serverlogger").logger.info("下注5")
            for betScore in betScoreAction.betScore:
                gl.get_v("serverlogger").logger.info("下注6")
                if betScore.index != 0 and betScore.index != 1 and betScore.index != 2:
                    break
                if seat.playScore + betScore.score > seat.score:
                    break
                maxPlay = 0
                if betScore.index == 0:
                    maxPlay = room.positions[2].totalScore + room.positions[1].totalScore + room.bankerScore
                if betScore.index == 1:
                    maxPlay = room.positions[2].totalScore + room.positions[0].totalScore + room.bankerScore
                if betScore.index == 2:
                    maxPlay = int(
                        ((room.positions[0].totalScore + room.positions[1].totalScore + room.bankerScore) * (
                                1 - pingReturn) + room.bankerScore) / pingRatio)
                if room.positions[betScore.index].totalScore + betScore.score > maxPlay:
                    break
                gl.get_v("serverlogger").logger.info("下注7")
                playPosition = room.positions[betScore.index]
                playPosition.totalScore += betScore.score
                if userId in playPosition.playScores:
                    playPosition.playScores[userId] += betScore.score
                else:
                    playPosition.playScores[userId] = betScore.score
                seat.playScore += betScore.score
                betScore.playerId = userId
                room.betScores.append(betScore.SerializeToString())
                gl.get_v("serverlogger").logger.info("下注8")
            gl.get_v("serverlogger").logger.info("下注成功")
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
