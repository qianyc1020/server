# coding=utf-8
from game.douniu.command.game import dealcard_cmd
from game.douniu.mode.game_status import GameStatus
from protocol.base.base_pb2 import START_GAME


def execute(room, messageHandle):
    if room.gameStatus == GameStatus.WAITING:
        for seat in room.seats:
            seat.ready = False
            seat.guanzhan = False
        messageHandle.broadcast_seat_to_gateway(START_GAME, None, room)

        if room.gameType == 0:
            dealcard_cmd.execute(room, messageHandle)
