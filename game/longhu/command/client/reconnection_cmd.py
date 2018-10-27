# coding=utf-8
import traceback
from decimal import Decimal

import core.globalvar as gl
from game.longhu.mode.game_status import GameStatus
from game.longhu.mode.longhu_room import LonghuRoom
from protocol.base.base_pb2 import REENTER_GAME, SELF_INFO, SELF_PLAYED
from protocol.base.game_base_pb2 import RecReEnterGame, RecUpdateGameUsers
from protocol.game.longfeng_pb2 import BaiRenLongFengScore


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)
            seat = room.getWatchSeatByUserId(userId)
            if seat is None:
                return
            room.sendBetScore()
            redis.setobj("room_" + str(roomNo), room)
            recReEnterGame = RecReEnterGame()
            recReEnterGame.gameState = room.gameStatus
            recReEnterGame.state = True
            recReEnterGame.curPlayCount = room.gameCount
            messageHandle.send_to_gateway(REENTER_GAME, recReEnterGame)

            room.recUpdateGameInfo(messageHandle)

            if room.getSeatByUserId(userId) is not None:
                room.recUpdateScore(messageHandle, 0)

                s = room.getSeatByUserId(userId)
                userInfo = RecUpdateGameUsers.UserInfo()
                userInfo.account = s.account
                userInfo.playerId = s.userId
                userInfo.headUrl = s.head
                userInfo.createTime = s.createDate
                userInfo.ip = s.ip
                userInfo.online = s.online
                userInfo.nick = s.nickname
                userInfo.ready = s.ready
                userInfo.score = int((s.score - s.playScore).quantize(Decimal('0')))
                userInfo.sex = s.sex
                userInfo.totalCount = s.total_count
                userInfo.loc = s.seatNo
                userInfo.consumeVip = s.level
                messageHandle.send_to_gateway(SELF_INFO, userInfo)
                room.updateBankerList(messageHandle, userId)
            else:
                room.recUpdateScore(messageHandle, userId)
                room.updateBankerList(messageHandle, userId)
            room.updateTrend(messageHandle, userId)
            room.updateWatchSize(messageHandle, userId)
            if room.gameStatus != GameStatus.WAITING:
                room.recReEnterGameInfo(messageHandle, userId)
                if seat.playScore > 0:
                    score = BaiRenLongFengScore()
                    for position in room.positions:
                        score.score.append(0 if userId in position.playScores[userId] else position.playScores[userId])
                    messageHandle.send_to_gateway(SELF_PLAYED, score)
            else:
                if room.started:
                    room.recReEnterGameInfo(messageHandle, userId)
                    if seat.playScore > 0:
                        score = BaiRenLongFengScore()
                        for position in room.positions:
                            score.score.append(
                                0 if userId in position.playScores[userId] else position.playScores[userId])
                        messageHandle.send_to_gateway(SELF_PLAYED, score)
                    room.executeAsk(messageHandle, userId, 1)

            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
