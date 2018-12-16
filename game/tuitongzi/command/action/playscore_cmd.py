# coding=utf-8
import traceback

import core.globalvar as gl
from game.tuitongzi.command.game import dealcard_cmd
from game.tuitongzi.mode.game_status import GameStatus
from protocol.game.bairen_pb2 import BaiRenBetScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    betScoreAction = BaiRenBetScoreAction()
    betScoreAction.ParseFromString(message)
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
            total = 0
            for p in room.positions:
                total += p.totalScore
            for betScore in betScoreAction.betScore:
                if 0 > betScore.index > 3:
                    break
                if seat.playScore + betScore.score > seat.score:
                    break
                total += betScore.score
                if total > room.bankerScore:
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
                if room.bankerScore - total - betScore.score < 100:
                    dealcard_cmd.execute(room, messageHandle)
                    break
            gl.get_v("serverlogger").logger.info("下注成功")
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
