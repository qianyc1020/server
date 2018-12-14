# coding=utf-8
import traceback

import core.globalvar as gl
from game.wuziqi.mode.game_status import GameStatus
from protocol.base.base_pb2 import GAME_OVER
from protocol.base.game_base_pb2 import RecGameOver


def execute(room, messageHandle):
    roomOver = RecGameOver()
    room.allocId = 3
    roomOver.gameId = room.roomNo
    messageHandle.broadcast_seat_to_gateway(GAME_OVER, roomOver, room)

    redis = gl.get_v("redis")
    for s in room.seats:
        redis.delobj(str(s.userId) + "_room")

    room.gameStatus = GameStatus.DESTORY

    redis.lock("lock3_rooms")
    try:
        if redis.exists("3_rooms"):
            rooms = redis.get("3_rooms")
            rooms.remove(room.roomNo)
            redis.delobj("room_" + str(room.roomNo))
            redis.delobj(str(room.roomNo) + "_gameId")
            redis.set("3_rooms", rooms)
    except:
        traceback.print_exc()
    redis.unlock("lock3_rooms")
