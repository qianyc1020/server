# coding=utf-8
from game.jinhua.command.game import dealcard_cmd
from game.jinhua.mode.game_status import GameStatus
from protocol.base.base_pb2 import START_GAME


def execute(room, messageHandle):
    if room.gameStatus == GameStatus.WAITING:
        for seat in room.seats:
            seat.ready = False
            seat.guanzhan = False
        messageHandle.broadcast_seat_to_gateway(START_GAME, None, room)
        room.bankerConfirm(messageHandle)
        room.gameStatus = GameStatus.PLAYING
        dealcard_cmd.execute(room, messageHandle)
        room.executeRound(messageHandle, 0)
