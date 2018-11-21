# coding=utf-8
import traceback

import core.globalvar as gl
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.mode.hongbao_room import HongbaoRoom
from protocol.base.base_pb2 import REENTER_GAME, SELF_INFO
from protocol.base.game_base_pb2 import RecReEnterGame, RecUpdateGameUsers


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")

        gameid = redis.get(str(roomNo) + "_gameId")
        if 11 != gameid:
            return

        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            seat = room.getWatchSeatByUserId(userId)
            if seat is not None:
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
                room.updateWatchSize(messageHandle, userId)
                if room.started:
                    room.recReEnterGameInfo(messageHandle, userId)
                    room.executeAsk(messageHandle, userId, 2)
                elif room.gameStatus != GameStatus.WAITING and userId == room.banker:
                    room.recReEnterGameInfo(messageHandle, userId)
                    room.executeAsk(messageHandle, userId, 1)

                redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
