# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from protocol.base.base_pb2 import GAME_OVER
from protocol.base.game_base_pb2 import RecGameOver


def execute(room, messageHandle):
    roomOver = RecGameOver()
    room.allocId = 2
    roomOver.gameId = room.roomNo
    messageHandle.broadcast_seat_to_gateway(GAME_OVER, roomOver, room)

    redis = gl.get_v("redis")
    for s in room.seats:
        redis.delobj(str(s.userId) + "_room")

    room.gameStatus = GameStatus.DESTORY

    redis.lock("lock2_rooms")
    try:
        if redis.exists("2_rooms"):
            rooms = redis.get("2_rooms")
            rooms.remove(room.roomNo)
            redis.delobj("room_" + str(room.roomNo))
            redis.delobj(str(room.roomNo) + "_gameId")
            redis.set("2_rooms", rooms)
    except:
        traceback.print_exc()
    redis.unlock("lock2_rooms")
