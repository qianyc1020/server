# coding=utf-8
import traceback

import core.globalvar as gl
from game.niuniu.command.game import dealcard_cmd
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.mode.niuniu_room import NiuniuRoom
from protocol.game.bairen_pb2 import BaiRenBetScoreAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), NiuniuRoom(), NiuniuRoom().object_to_dict)
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
            betScoreAction = BaiRenBetScoreAction()
            betScoreAction.ParseFromString(message)
            for betScore in betScoreAction.betScore:
                if 0 > betScore.index > 3:
                    break
                if seat.playScore + betScore.score > seat.score:
                    break
                total = 0
                for p in room.positions:
                    total += p.totalScore

                if total + betScore.score > room.bankerScore / 3:
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

                if room.bankerScore / 3 - total - betScore.score < 100:
                    dealcard_cmd.execute(room, messageHandle)
                    break

            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
