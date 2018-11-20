# coding=utf-8
import time
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.tuitongzi.mode.game_status import GameStatus
from game.tuitongzi.mode.tuitongzi_seat import TuitongziSeat
from protocol.base.base_pb2 import GAME_SVR_MATCH
from protocol.base.game_base_pb2 import RecMatchGame
from protocol.service.match_pb2 import ReqApplyEnterMatch


def execute(userId, message, messageHandle, room):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        return

    account = data_account.query_account_by_id(None, userId)

    reqApplyEnterMatch = ReqApplyEnterMatch()
    reqApplyEnterMatch.ParseFromString(message.data)


    recMatchGame = RecMatchGame()
    recMatchGame.allocId = 7
    recMatchGame.level = reqApplyEnterMatch.level

    messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)

    tuitongziSeat = TuitongziSeat()
    tuitongziSeat.seatNo = 0
    tuitongziSeat.userId = account.id
    tuitongziSeat.account = account.account_name
    tuitongziSeat.createDate = account.create_time
    tuitongziSeat.nickname = account.nick_name
    tuitongziSeat.head = account.head_url
    tuitongziSeat.sex = account.sex
    tuitongziSeat.score = int(account.gold.quantize(Decimal('0')))
    tuitongziSeat.ip = account.last_address
    tuitongziSeat.gpsInfo = ""
    tuitongziSeat.total_count = account.total_count
    tuitongziSeat.introduce = account.introduce
    tuitongziSeat.phone = account.phone
    tuitongziSeat.level = account.level
    tuitongziSeat.experience = account.experience
    tuitongziSeat.intoDate = int(time.time())
    room.watchSeats.append(tuitongziSeat)
    room.sendBetScore(messageHandle)

    room.recUpdateGameInfo(messageHandle)
    room.recUpdateScore(messageHandle, userId)
    room.updateBankerList(messageHandle, userId)
    room.updateWatchSize(messageHandle, 0)
    room.updateTrend(messageHandle, userId)
    if 0 == room.gameStatus == GameStatus.PLAYING or room.started:
        room.recReEnterGameInfo(messageHandle, userId)
        if room.gameStatus == GameStatus.PLAYING:
            room.executeAsk(messageHandle, userId, 2)
        else:
            room.executeAsk(messageHandle, userId, 1)
    redis.set(str(userId) + "_room", room.roomNo)
    redis.setobj("room_" + str(room.roomNo), room)
