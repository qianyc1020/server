# coding=utf-8
import threading
import time

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from game.jinhua.server.command import record_cmd
from game.jinhua.timeout import ready_timeout
from mode.base.create_game_details import CreateGameDetails
from mode.base.rebate import Rebate
from mode.base.update_currency import UpdateCurrency
from protocol.base.base_pb2 import SETTLE_GAME
from protocol.base.game_base_pb2 import RecSettleSingle
from protocol.game.jinhua_pb2 import JinhuaPlayerOneSetResult


def execute(room, messageHandle, wins):
    if room.gameStatus == GameStatus.PLAYING:
        recSettleSingle = RecSettleSingle()
        recSettleSingle.allocId = 1
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())

        kou = False
        scores = ""
        users = ""
        rebates = []
        update_currency = []
        game_details = []
        for s in room.seats:
            jinhuaPlayerOneSetResult = JinhuaPlayerOneSetResult()
            for s1 in room.seats:
                if not s1.guanzhan:
                    if s1 in wins:
                        winOrLose = room.deskScore / len(wins) - s1.playScore
                    else:
                        winOrLose = -s1.playScore
                    jinhuaSettlePlayerInfo = jinhuaPlayerOneSetResult.players.add()
                    jinhuaSettlePlayerInfo.playerId = s1.userId
                    jinhuaSettlePlayerInfo.score = winOrLose
                    if not kou:
                        s1.score += winOrLose
                        scores += "," + str(winOrLose)
                        users += "," + str(s1.userId)

                        update_currency.append(UpdateCurrency(winOrLose, s1.userId, room.roomNo))
                        game_details.append(CreateGameDetails(s1.userId, 1, str(room.roomNo), winOrLose,
                                                              int(0.5 * room.score), int(time.time())))
                        rebate = Rebate()
                        rebate.userId = s1.userId
                        rebate.card = int(0.5 * room.score)
                        rebates.append(rebate)
                    if s1.userId in s.canLookUser or s.userId == s1.userId:
                        jinhuaSettlePlayerInfo.card.extend(s1.initialCards)
                    else:
                        jinhuaSettlePlayerInfo.card.extend([0, 0, 0])
                    jinhuaSettlePlayerInfo.totalScore = s1.score
            kou = True
            recSettleSingle.content = jinhuaPlayerOneSetResult.SerializeToString()
            messageHandle.send_to_gateway(SETTLE_GAME, recSettleSingle, s.userId)

        gl.get_v("rebate-handle-queue").put(rebates)
        if 0 != len(update_currency):
            gl.get_v("update_currency").putall(update_currency)
        if 0 != len(game_details):
            gl.get_v("game_details").putall(game_details)
        record_cmd.execute(room, users[1:], scores[1:])
        room.clear()

        levelSeat = []
        for s in room.seats:
            if s.score < room.leaveScore or not s.online:
                levelSeat.append(s.userId)
        for l in levelSeat:
            room.exit(l, messageHandle)
        if len(wins) != 0:
            room.banker = wins[0].userId
        room.gameCount += 1
        for seat in room.seats:
            threading.Thread(target=ready_timeout.execute,
                                 args=(room.gameCount, room.roomNo, messageHandle, seat.userId, seat.intoDate),
                                 name='ready_timeout').start()  # 线程对象.
