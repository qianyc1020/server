# coding=utf-8
import time
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.mode.hongbao_seat import HongbaoSeat
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
    recMatchGame.allocId = 11
    recMatchGame.level = reqApplyEnterMatch.level

    messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)

    if room.getWatchSeatByUserId(userId) is None:
        hongbaoSeat = HongbaoSeat()
        hongbaoSeat.seatNo = 0
        hongbaoSeat.userId = account.id
        hongbaoSeat.account = account.account_name
        hongbaoSeat.createDate = account.create_time
        hongbaoSeat.nickname = account.nick_name
        hongbaoSeat.head = account.head_url
        hongbaoSeat.sex = account.sex
        hongbaoSeat.score = int(account.gold.quantize(Decimal('0')))
        hongbaoSeat.ip = account.last_address
        hongbaoSeat.gpsInfo = ""
        hongbaoSeat.total_count = account.total_count
        hongbaoSeat.introduce = account.introduce
        hongbaoSeat.phone = account.phone
        hongbaoSeat.level = account.level
        hongbaoSeat.experience = account.experience
        hongbaoSeat.intoDate = int(time.time())
        room.watchSeats.append(hongbaoSeat)

    room.recUpdateGameInfo(messageHandle)
    room.recUpdateScore(messageHandle, userId)
    room.updateBankerList(messageHandle, userId)
    room.updateWatchSize(messageHandle, 0)
    if 0 == room.gameStatus == GameStatus.PLAYING or room.started:
        room.recReEnterGameInfo(messageHandle, userId)
        if room.started:
            room.executeAsk(messageHandle, userId, 2)
    redis.set(str(userId) + "_room", room.roomNo)
    room.save(redis)
