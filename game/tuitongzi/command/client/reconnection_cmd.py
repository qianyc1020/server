# coding=utf-8
import traceback

import core.globalvar as gl
from game.tuitongzi.mode.game_status import GameStatus
from protocol.base.base_pb2 import REENTER_GAME, SELF_INFO, SELF_PLAYED
from protocol.base.game_base_pb2 import RecReEnterGame, RecUpdateGameUsers
from protocol.game.bairen_pb2 import BaiRenScore


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")

        gameid = redis.get(str(roomNo) + "_gameId")
        if 7 != gameid:
            return

        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            seat = room.getWatchSeatByUserId(userId)
            if seat is not None:
                room.sendBetScore(messageHandle)
                room.save(redis)
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
                    userInfo.score = s.score - s.playScore
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
                        score = BaiRenScore()
                        for position in room.positions:
                            score.score.append(0 if userId not in position.playScores else position.playScores[userId])
                        messageHandle.send_to_gateway(SELF_PLAYED, score)
                    room.executeAsk(messageHandle, userId, 2)
                else:
                    if room.started:
                        room.recReEnterGameInfo(messageHandle, userId)
                        if seat.playScore > 0:
                            score = BaiRenScore()
                            for position in room.positions:
                                score.score.append(
                                    0 if userId not in position.playScores else position.playScores[userId])
                            messageHandle.send_to_gateway(SELF_PLAYED, score)
                        room.executeAsk(messageHandle, userId, 1)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
