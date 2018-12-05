# coding=utf-8
import time
import traceback
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.wuziqi.mode.wuziqi_room import WuziqiRoom
from game.wuziqi.mode.wuziqi_seat import WuziqiSeat
from protocol.base.base_pb2 import RecJoinGame, JOIN_GAME, ReqJoinGame


def joinGame(room, messageHandle, userId, redis):
    recJoinGame = RecJoinGame()
    recJoinGame.gameId = room.roomNo

    if len(room.seatNos) != 0 and room.getSeatByUserId(userId) is None:
        account = data_account.query_account_by_id(None, userId)
        wuziqiSeat = WuziqiSeat()
        wuziqiSeat.seatNo = room.seatNos[0]
        room.seatNos.remove(room.seatNos[0])
        wuziqiSeat.userId = account.id
        wuziqiSeat.account = account.account_name
        wuziqiSeat.createDate = account.create_time
        wuziqiSeat.nickname = account.nick_name
        wuziqiSeat.head = account.head_url
        wuziqiSeat.sex = account.sex
        wuziqiSeat.score = int(account.gold.quantize(Decimal('0')))
        wuziqiSeat.ip = account.last_address
        wuziqiSeat.gpsInfo = ""
        wuziqiSeat.total_count = account.total_count
        wuziqiSeat.introduce = account.introduce
        wuziqiSeat.phone = account.phone
        wuziqiSeat.level = account.level
        wuziqiSeat.experience = account.experience
        wuziqiSeat.intoDate = int(time.time())
        room.seats.append(wuziqiSeat)
    else:
        recJoinGame.state = 2
    if 1 != len(room.seatNos):
        messageHandle.send_to_gateway(JOIN_GAME, recJoinGame)

    room.recUpdateGameInfo(messageHandle)
    room.recUpdateScore(messageHandle, 0)
    if 0 != room.score:
        room.recReEnterGameInfo(messageHandle, userId)

    redis.set(str(userId) + "_room", room.roomNo)
    room.save(redis)


def execute(userId, message, messageHandle, room=None):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        return

    if room is not None:
        joinGame(room, messageHandle, userId, redis)
    else:
        reqJoinGame = ReqJoinGame()
        reqJoinGame.ParseFromString(message.data)
        roomNo = reqJoinGame.gameId
        gameid = redis.get(str(roomNo) + "_gameId")
        if 3 != gameid:
            return
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), WuziqiRoom(), WuziqiRoom().object_to_dict)
            joinGame(room, messageHandle, userId, redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
