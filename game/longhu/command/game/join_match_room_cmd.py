# coding=utf-8
import time
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.longhu.mode.game_status import GameStatus
from game.longhu.mode.longhu_seat import LonghuSeat
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
    recMatchGame.allocId = 8
    recMatchGame.level = reqApplyEnterMatch.level

    messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)

    if room.getWatchSeatByUserId(userId) is None:
        longhuSeat = LonghuSeat()
        longhuSeat.seatNo = 0
        longhuSeat.userId = account.id
        longhuSeat.account = account.account_name
        longhuSeat.createDate = account.create_time
        longhuSeat.nickname = account.nick_name
        longhuSeat.head = account.head_url
        longhuSeat.sex = account.sex
        longhuSeat.score = int(account.gold.quantize(Decimal('0')))
        longhuSeat.ip = account.last_address
        longhuSeat.gpsInfo = ""
        longhuSeat.total_count = account.total_count
        longhuSeat.introduce = account.introduce
        longhuSeat.phone = account.phone
        longhuSeat.level = account.level
        longhuSeat.experience = account.experience
        longhuSeat.intoDate = int(time.time())
        room.watchSeats.append(longhuSeat)
    room.sendBetScore(messageHandle)

    room.recUpdateGameInfo(messageHandle)
    room.recUpdateScore(messageHandle, 0)
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
