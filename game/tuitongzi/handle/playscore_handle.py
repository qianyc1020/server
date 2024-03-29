# coding=utf-8
import Queue
import traceback

import core.globalvar as gl
from game.tuitongzi.mode.game_status import GameStatus


class PlayScoreHandle(object):

    def __init__(self, roomNo, queue, messageHandle):
        self._close = False
        self.roomNo = roomNo
        self.queue = queue
        self.messageHandle = messageHandle

    def close(self):
        self._close = True

    def execute(self):
        from game.tuitongzi.command.game import dealcard_cmd
        redis = gl.get_v("redis")
        while not self._close:
            try:
                playScores = self.queue.getall(35, True, 20)
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
                            return
                        seat = room.getWatchSeatByUserId(p.userId)
                        if seat is None:
                            redis.unlock("lockroom_" + self.roomNo)
                            return
                        total = 0
                        for b in room.positions:
                            total += b.totalScore
                        for betScore in p.betScoreAction.betScore:
                            if 1 > betScore.index > 3:
                                break
                            if seat.playScore + betScore.score > seat.score:
                                break
                            total += betScore.score
                            if total > room.bankerScore:
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
                            if room.bankerScore - total - betScore.score < 100:
                                dealcard_cmd.execute(room, self.messageHandle)
                                break
                    gl.get_v("serverlogger").logger.info("下注成功")
                    room.save(redis)
                except:
                    print traceback.print_exc()
                redis.unlock("lockroom_" + self.roomNo)
            except Queue.Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
