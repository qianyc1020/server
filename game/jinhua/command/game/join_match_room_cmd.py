# coding=utf-8
import threading
import time
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.jinhua.mode.game_status import GameStatus
from game.jinhua.mode.jinhua_seat import JinhuaSeat
from game.jinhua.timeout import ready_timeout
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
    recMatchGame.allocId = 1
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
        jinhuaSeat = JinhuaSeat()
        jinhuaSeat.seatNo = room.seatNos[0]
        room.seatNos.remove(room.seatNos[0])
        jinhuaSeat.userId = account.id
        jinhuaSeat.account = account.account_name
        jinhuaSeat.createDate = account.create_time
        jinhuaSeat.nickname = account.nick_name
        jinhuaSeat.head = account.head_url
        jinhuaSeat.sex = account.sex
        jinhuaSeat.score = int(account.gold.quantize(Decimal('0')))
        jinhuaSeat.ip = account.last_address
        jinhuaSeat.gpsInfo = ""
        jinhuaSeat.total_count = account.total_count
        jinhuaSeat.introduce = account.introduce
        jinhuaSeat.phone = account.phone
        jinhuaSeat.level = account.level
        jinhuaSeat.experience = account.experience
        jinhuaSeat.intoDate = int(time.time())
        jinhuaSeat.guanzhan = room.gameStatus == GameStatus.PLAYING
        room.seats.append(jinhuaSeat)

        t = threading.Thread(target=ready_timeout.execute,
                             args=(room.gameCount, room.roomNo, messageHandle, userId, jinhuaSeat.intoDate),
                             name='ready_timeout')  # 线程对象.
        t.start()

    room.recUpdateGameInfo(messageHandle)
    room.recUpdateScore(messageHandle, 0)
    if room.gameStatus == GameStatus.PLAYING:
        room.recReEnterGameInfo(messageHandle, userId)
    redis.set(str(userId) + "_room", room.roomNo)
    room.save(redis)
