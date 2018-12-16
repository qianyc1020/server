# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from protocol.game.jinhua_pb2 import JinhuaCompare


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        jinhuaCompare = JinhuaCompare()
        jinhuaCompare.ParseFromString(message)
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("比牌失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and seat.seatNo == room.operationSeat and not seat.end:
                compareSeat = room.getSeatByUserId(jinhuaCompare.compareId)
                if compareSeat is not None and compareSeat != seat and not compareSeat.end:
                    compareScore = room.minScore
                    if seat.lookCard:
                        compareScore *= 2
                    if compareScore <= seat.score - seat.playScore:
                        seat.playScore += compareScore
                        room.deskScore += compareScore
                        seat.canLookUser.append(compareSeat.userId)
                        compareSeat.canLookUser.append(seat.userId)
                        settleResult = room.settle(seat, compareSeat)
                        if settleResult is not None:
                            jinhuaCompare.score = compareScore
                            if settleResult.userSettleResule[0].win > 0:
                                jinhuaCompare.win = True
                                compareSeat.end = True
                            else:
                                jinhuaCompare.win = False
                                seat.end = True
                            room.executeAction(seat.userId, 3, jinhuaCompare, messageHandle)
                        if not room.checkOver(messageHandle):
                            room.changeOperation()
                            room.executeRound(messageHandle, 0)
                            seat.round += 1
                            room.checkRound(messageHandle)

                        room.save(redis)

                    else:
                        gl.get_v("serverlogger").logger.info("比牌失败分数不够")
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
