# coding=utf-8
import traceback

import core.globalvar as gl
from game.longhu.mode.game_status import GameStatus
from protocol.base.base_pb2 import GAME_OVER
from protocol.base.game_base_pb2 import RecGameOver


def execute(room, messageHandle):
    roomOver = RecGameOver()
    room.allocId = 8
    roomOver.gameId = room.roomNo
    messageHandle.broadcast_watch_to_gateway(GAME_OVER, roomOver, room)

    redis = gl.get_v("redis")
    for s in room.watchSeats:
        redis.delobj(str(s.userId) + "_room")

    room.gameStatus = GameStatus.DESTORY

    redis.lock("lock8_rooms")
    try:
        if redis.exists("8_rooms"):
            rooms = redis.get("8_rooms")
            rooms.remove(room.roomNo)
            redis.delobj("room_" + str(room.roomNo))
            redis.delobj(str(room.roomNo) + "_gameId")
            redis.set("8_rooms", rooms)
    except:
        traceback.print_exc()
    redis.unlock("lock8_rooms")
