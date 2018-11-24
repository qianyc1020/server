# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from protocol.base.base_pb2 import GAME_OVER
from protocol.base.game_base_pb2 import RecGameOver


def execute(room, messageHandle):
    roomOver = RecGameOver()
    room.allocId = 1
    roomOver.gameId = room.roomNo
    messageHandle.broadcast_seat_to_gateway(GAME_OVER, roomOver, room)

    redis = gl.get_v("redis")
    for s in room.seats:
        redis.delobj(str(s.userId) + "_room")

    room.gameStatus = GameStatus.DESTORY

    redis.lock("lock1_rooms", 5000)
    try:
        if redis.exists("1_rooms"):
            rooms = redis.get("1_rooms")
            rooms.remove(room.roomNo)
            redis.delobj("room_" + str(room.roomNo))
            redis.delobj(str(room.roomNo) + "_gameId")
            redis.set("1_rooms", rooms)
    except:
        traceback.print_exc()
    redis.unlock("lock1_rooms")
