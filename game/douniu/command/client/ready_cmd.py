# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.command.game import gamestart_cmd
from game.douniu.mode.game_status import GameStatus
from game.douniu.mode.douniu_room import DouniuRoom
from protocol.base.base_pb2 import READY_GAME
from protocol.base.game_base_pb2 import RecReadyGame


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
            if room.gameStatus == GameStatus.WAITING:
                seat = room.getSeatByUserId(userId)
                if seat is not None and not seat.ready:
                    seat.ready = True
                recReadyGame = RecReadyGame()
                allReady = True
                for seat in room.seats:
                    if not seat.ready:
                        allReady = False
                    readyState = recReadyGame.list.add()
                    readyState.playerId = seat.userId
                    readyState.ready = seat.ready
                messageHandle.broadcast_seat_to_gateway(READY_GAME, recReadyGame, room)
                if allReady and len(room.seats) > 1:
                    gamestart_cmd.execute(room, messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
