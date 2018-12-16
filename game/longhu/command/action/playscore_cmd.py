# coding=utf-8
import traceback

import core.globalvar as gl
from core import config
from game.longhu.mode.game_status import GameStatus
from protocol.game.bairen_pb2 import BaiRenBetScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    betScoreAction = BaiRenBetScoreAction()
    betScoreAction.ParseFromString(message)
    pingReturn = float(config.get("longhu", "pingReturn"))
    pingRatio = float(config.get("longhu", "pingRatio"))
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
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
            for betScore in betScoreAction.betScore:
                if betScore.index != 0 and betScore.index != 1 and betScore.index != 2:
                    break
                if seat.playScore + betScore.score > seat.score:
                    break
                maxPlay = 0
                if betScore.index == 0:
                    maxPlay = room.positions[2].totalScore + room.positions[1].totalScore + room.bankerScore
                elif betScore.index == 1:
                    maxPlay = room.positions[2].totalScore + room.positions[0].totalScore + room.bankerScore
                elif betScore.index == 2:
                    maxPlay = int(
                        ((room.positions[0].totalScore + room.positions[1].totalScore + room.bankerScore) * (
                                1 - pingReturn) + room.bankerScore) / pingRatio)
                if room.positions[betScore.index].totalScore + betScore.score > maxPlay:
                    break
                playPosition = room.positions[betScore.index]
                playPosition.totalScore += betScore.score
                if userId in playPosition.playScores:
                    playPosition.playScores[userId] += betScore.score
                else:
                    playPosition.playScores[userId] = betScore.score
                seat.playScore += betScore.score
                betScore.playerId = userId
                room.betScores.append(betScore.SerializeToString())
            gl.get_v("serverlogger").logger.info("下注成功")
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
