# coding=utf-8
import threading
import time

from data.database import data_game_details
from game.jinhua.mode.game_status import GameStatus
from game.jinhua.server.command import record_cmd
from game.jinhua.timeout import ready_timeout
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
                        messageHandle.game_update_currency(winOrLose, s1.userId, room.roomNo)
                        data_game_details.create_game_details(s1.userId, 1, str(room.roomNo), winOrLose,
                                                              int(0.5 * room.score), int(time.time()))
                    if s1.userId in s.canLookUser or s.userId == s1.userId:
                        jinhuaSettlePlayerInfo.card.extend(s1.initialCards)
                    else:
                        jinhuaSettlePlayerInfo.card.extend([0, 0, 0])
                    jinhuaSettlePlayerInfo.totalScore = s1.score
            kou = True
            recSettleSingle.content = jinhuaPlayerOneSetResult.SerializeToString()
            messageHandle.send_to_gateway(SETTLE_GAME, recSettleSingle, s.userId)
        record_cmd.execute(room, users[1:], scores[1:])
        room.clear()

        levelSeat = []
        for s in room.seats:
            if s.score < room.leaveScore:
                levelSeat.append(s.userId)
        for l in levelSeat:
            room.exit(l, messageHandle)
        if len(wins) != 0:
            room.banker = wins[0].userId
        room.gameCount += 1
        for seat in room.seats:
            t = threading.Thread(target=ready_timeout.execute,
                                 args=(room.gameCount, room.roomNo, messageHandle, seat.userId, seat.intoDate),
                                 name='ready_timeout')  # 线程对象.
            t.start()
