# coding=utf-8
import random
import traceback

import core.globalvar as gl
from game.wuziqi.command.client import join_room_cmd
from game.wuziqi.mode.wuziqi_room import WuziqiRoom
from protocol.base.base_pb2 import RecCreateGame, CREATE_GAME


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        return
    room = WuziqiRoom()
    redis.lock("lock3_rooms", 5000)
    try:
        if redis.exists("3_rooms"):
            rooms = redis.get("3_rooms")
        else:
            rooms = []
        roomNo = random.randint(100000, 999999)
        while roomNo in rooms:
            roomNo = random.randint(100000, 999999)
        rooms.append(roomNo)
        room.roomNo = roomNo
        redis.setobj("room_" + str(roomNo), room)
        redis.set(str(roomNo) + "_gameId", 3)
        redis.set("3_rooms", rooms)
        recCreateGame = RecCreateGame()
        recCreateGame.gameId = roomNo
        messageHandle.send_to_gateway(CREATE_GAME, recCreateGame)
        redis.lock("lockroom_" + str(roomNo), 5000)
        join_room_cmd.execute(userId, message, messageHandle, room)
        redis.unlock("lockroom_" + str(roomNo))
    except:
        traceback.print_exc()
    redis.unlock("lock3_rooms")
