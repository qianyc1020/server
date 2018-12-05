# coding=utf-8
import threading
import time
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.douniu.mode.game_status import GameStatus
from game.douniu.mode.douniu_seat import DouniuSeat
from game.douniu.timeout import ready_timeout
from protocol.base.base_pb2 import GAME_SVR_MATCH
from protocol.base.game_base_pb2 import RecMatchGame
from protocol.service.match_pb2 import ReqApplyEnterMatch


def execute(userId, message, messageHandle, room):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        return

    reqApplyEnterMatch = ReqApplyEnterMatch()
    reqApplyEnterMatch.ParseFromString(message.data)

    recMatchGame = RecMatchGame()
    recMatchGame.allocId = 2
    recMatchGame.level = reqApplyEnterMatch.level

    account = data_account.query_account_by_id(None, userId)
    if account.gold < room.inScore:
        recMatchGame.state = 1
        messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)
        return

    if len(room.seatNos) == 0:
        recMatchGame.state = 3
        messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)
        return

    messageHandle.send_to_gateway(GAME_SVR_MATCH, recMatchGame)

    if room.getSeatByUserId(userId) is None:
        douniuSeat = DouniuSeat()
        douniuSeat.seatNo = room.seatNos[0]
        room.seatNos.remove(room.seatNos[0])
        douniuSeat.userId = account.id
        douniuSeat.account = account.account_name
        douniuSeat.createDate = account.create_time
        douniuSeat.nickname = account.nick_name
        douniuSeat.head = account.head_url
        douniuSeat.sex = account.sex
        douniuSeat.score = int(account.gold.quantize(Decimal('0')))
        douniuSeat.ip = account.last_address
        douniuSeat.gpsInfo = ""
        douniuSeat.total_count = account.total_count
        douniuSeat.introduce = account.introduce
        douniuSeat.phone = account.phone
        douniuSeat.level = account.level
        douniuSeat.experience = account.experience
        douniuSeat.intoDate = int(time.time())
        douniuSeat.guanzhan = room.gameStatus > GameStatus.WAITING
        room.seats.append(douniuSeat)

        t = threading.Thread(target=ready_timeout.execute,
                             args=(room.gameCount, room.roomNo, messageHandle, userId, douniuSeat.intoDate),
                             name='ready_timeout')  # 线程对象.
        t.start()

    room.recUpdateGameInfo(messageHandle)
    room.recUpdateScore(messageHandle, 0)
    if room.gameStatus == GameStatus.PLAYING:
        room.recReEnterGameInfo(messageHandle, userId)
    redis.set(str(userId) + "_room", room.roomNo)
    room.save(redis)
