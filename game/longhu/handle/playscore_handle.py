# coding=utf-8
import Queue
import traceback

import core.globalvar as gl
from core import config
from game.longhu.mode.game_status import GameStatus


class PlayScoreHandle(object):

    def __init__(self, roomNo, queue):
        self._close = False
        self.roomNo = roomNo
        self.queue = queue

    def close(self):
        self._close = True

    def execute(self):
        redis = gl.get_v("redis")
        pingReturn = float(config.get("longhu", "pingReturn"))
        pingRatio = float(config.get("longhu", "pingRatio"))
        while not self._close:
            try:
                playScores = self.queue.getall(True, 20)
                redis.lock("lockroom_" + self.roomNo)
                try:
                    room = redis.getobj("room_" + self.roomNo)
                    if room.gameStatus != GameStatus.PLAYING:
                        gl.get_v("serverlogger").logger.info("下注失败状态不对")
                        redis.unlock("lockroom_" + self.roomNo)
                        return
                    for p in playScores:
                        if p.userId == room.banker:
                            redis.unlock("lockroom_" + self.roomNo)
                            break
                        seat = room.getWatchSeatByUserId(p.userId)
                        if seat is None:
                            redis.unlock("lockroom_" + self.roomNo)
                            break
                        for betScore in p.betScoreAction.betScore:
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
                                    ((room.positions[0].totalScore + room.positions[
                                        1].totalScore + room.bankerScore) * (
                                             1 - pingReturn) + room.bankerScore) / pingRatio)
                            if room.positions[betScore.index].totalScore + betScore.score > maxPlay:
                                break
                            playPosition = room.positions[betScore.index]
                            playPosition.totalScore += betScore.score
                            if p.userId in playPosition.playScores:
                                playPosition.playScores[p.userId] += betScore.score
                            else:
                                playPosition.playScores[p.userId] = betScore.score
                            seat.playScore += betScore.score
                            betScore.playerId = p.userId
                            room.betScores.append(betScore.SerializeToString())
                    gl.get_v("serverlogger").logger.info("下注成功")
                    room.save(redis)
                except:
                    print traceback.print_exc()
                redis.unlock("lockroom_" + self.roomNo)
            except Queue.Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
