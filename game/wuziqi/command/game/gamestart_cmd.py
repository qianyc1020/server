# coding=utf-8

from game.wuziqi.mode.game_status import GameStatus
from protocol.base.base_pb2 import START_GAME


def execute(room, messageHandle):
    if room.gameStatus == GameStatus.WAITING:
        room.gameStatus = GameStatus.PLAYING
        for seat in room.seats:
            seat.ready = False
        messageHandle.broadcast_seat_to_gateway(START_GAME, None, room)
