# coding=utf-8
import time

import core.globalvar as gl
from game.wuziqi.command.game import roomover_cmd
from game.wuziqi.mode.game_status import GameStatus
from game.wuziqi.server.command import record_cmd
from mode.base.create_game_details import CreateGameDetails
from mode.base.update_currency import UpdateCurrency
from protocol.base.base_pb2 import SETTLE_GAME
from protocol.base.game_base_pb2 import RecSettleSingle
from protocol.game.bairen_pb2 import BaiRenPlayerOneSetResult


def execute(room, messageHandle, userId):
    if room.gameStatus == GameStatus.PLAYING:

        wuziqiPlayerOneSetResult = BaiRenPlayerOneSetResult()

        amount = room.score
        seat = room.getSeatByUserId(userId)
        if seat is not None:
            if seat.score < amount:
                amount = seat.score

        scores = ""
        users = ""
        update_currency = []
        game_details = []
        for seat in room.seats:
            users += "," + str(seat.userId)
            win = 0
            if seat.userId != userId:
                win = amount
            else:
                win = -amount

            seat.score += win
            scores += "," + str(win)
            update_currency.append(UpdateCurrency(win, seat.userId, room.roomNo))
            game_details.append(CreateGameDetails(seat.userId, 3, str(room.roomNo), win, 0, int(time.time())))

            daerSettlePlayerInfo = wuziqiPlayerOneSetResult.players.add()
            daerSettlePlayerInfo.playerId = seat.userId
            daerSettlePlayerInfo.score = seat.score
            daerSettlePlayerInfo.totalScore = win
            gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (seat.userId, seat.score))

        recSettleSingle = RecSettleSingle()
        recSettleSingle.allocId = 3
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())
        recSettleSingle.content = wuziqiPlayerOneSetResult.SerializeToString()
        messageHandle.broadcast_seat_to_gateway(SETTLE_GAME, recSettleSingle, room)

        if len(users) > 0:
            if 0 != len(update_currency):
                gl.get_v("update_currency").putall(update_currency)
            if 0 != len(game_details):
                gl.get_v("game_details").putall(game_details)
            record_cmd.execute(room, users[1:], scores[1:])
        if 0 != len(room.seats):
            room.clear()
            room.gameCount += 1
        else:
            roomover_cmd.execute(room, messageHandle)
