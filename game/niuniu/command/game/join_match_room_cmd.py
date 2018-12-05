# coding=utf-8
import time
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.mode.niuniu_seat import NiuniuSeat
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
    recMatchGame.allocId = 10
    recMatchGame.level = reqApplyEnterMatch.level

    messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)

    if room.getWatchSeatByUserId(userId) is None:
        niuniuSeat = NiuniuSeat()
        niuniuSeat.seatNo = 0
        niuniuSeat.userId = account.id
        niuniuSeat.account = account.account_name
        niuniuSeat.createDate = account.create_time
        niuniuSeat.nickname = account.nick_name
        niuniuSeat.head = account.head_url
        niuniuSeat.sex = account.sex
        niuniuSeat.score = int(account.gold.quantize(Decimal('0')))
        niuniuSeat.ip = account.last_address
        niuniuSeat.gpsInfo = ""
        niuniuSeat.total_count = account.total_count
        niuniuSeat.introduce = account.introduce
        niuniuSeat.phone = account.phone
        niuniuSeat.level = account.level
        niuniuSeat.experience = account.experience
        niuniuSeat.intoDate = int(time.time())
        room.watchSeats.append(niuniuSeat)
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
    room.save(redis)
