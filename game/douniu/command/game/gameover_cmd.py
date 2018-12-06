# coding=utf-8
import threading
import time

import grpc

from data.database import data_game_details
from game.douniu.mode.game_status import GameStatus
from game.douniu.server.command import record_cmd
from game.douniu.timeout import ready_timeout
from protocol.base.base_pb2 import SETTLE_GAME
from protocol.base.game_base_pb2 import RecSettleSingle
from protocol.game import zhipai_pb2_grpc
from protocol.game.douniu_pb2 import DouniuPlayerOneSetResult
from protocol.game.zhipai_pb2 import SettleData, NiuniuSettleData


def settle(room):
    settleData = SettleData()
    settleData.banker = room.banker
    for seat in room.seats:
        if not seat.guanzhan:
            userSettleData = settleData.userSettleData.add()
            userSettleData.userId = seat.userId
            userSettleData.cardlist.extend(seat.initialCards)
            userSettleData.score = seat.playScore
            userSettleData.grab = 1 if seat.grab < 1 else seat.grab
    niuniuSettleData = NiuniuSettleData()
    niuniuSettleData.gameRules = room.gameRules
    settleData.extraData = niuniuSettleData.SerializeToString()
    conn = grpc.insecure_channel('127.0.0.1:50002')
    client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
    settleResult = client.settle(settleData)

    return settleResult


def execute(room, messageHandle):
    if room.gameStatus == GameStatus.OPENING:

        settleResult = settle(room)
        winOrLose = {}
        win = {}
        lose = {}
        total = 0
        totalWin = 0
        totalLose = 0
        for userSettleResult in settleResult.userSettleResule:
            if userSettleResult.userId != room.banker:
                seat = room.getSeatByUserId(userSettleResult.userId)
                if seat.score < userSettleResult.win and userSettleResult.win > 0:
                    winOrLose[seat.userId] = seat.score
                    total -= seat.score
                elif -seat.score > userSettleResult.win and userSettleResult.win < 0:
                    winOrLose[seat.userId] = -seat.score
                    total += seat.score
                else:
                    winOrLose[seat.userId] = userSettleResult.win
                    total -= userSettleResult.win
                if userSettleResult.win > 0:
                    win[seat.userId] = winOrLose[seat.userId]
                    totalWin += win[seat.userId]
                else:
                    lose[seat.userId] = winOrLose[seat.userId]
                    totalLose -= lose[seat.userId]

        banker = room.getSeatByUserId(room.banker)
        if banker.score + total < 0:
            for (d, x) in win.items():
                winOrLose[d] = int(x / totalWin * (banker.score + totalLose))
        elif total > banker.score:
            for (d, x) in lose.items():
                winOrLose[d] = int(x / totalLose * (banker.score + totalWin))

        bankerWin = 0
        for (d, x) in winOrLose.items():
            bankerWin += x

        users = ""
        scores = ""
        douniuPlayerOneSetResult = DouniuPlayerOneSetResult()
        for userSettleResult in settleResult.userSettleResule:
            seat = room.getSeatByUserId(userSettleResult.userId)
            daerSettlePlayerInfo = douniuPlayerOneSetResult.players.add()
            daerSettlePlayerInfo.playerId = userSettleResult.userId
            daerSettlePlayerInfo.cardType = userSettleResult.cardValue
            daerSettlePlayerInfo.card.extend(seat.initialCards)
            users += "," + str(seat.userId)
            if userSettleResult.userId != room.banker:
                scores += "," + str(winOrLose[userSettleResult.userId])
                seat.score += winOrLose[userSettleResult.userId]
                daerSettlePlayerInfo.score = winOrLose[userSettleResult.userId]
                messageHandle.game_update_currency(winOrLose[userSettleResult.userId], seat.userId, room.roomNo)
                data_game_details.create_game_details(userSettleResult.userId, 2, str(room.roomNo),
                                                      winOrLose[userSettleResult.userId], int(0.5 * room.score),
                                                      int(time.time()))
            else:
                scores += "," + str(-bankerWin)
                seat.score -= bankerWin
                daerSettlePlayerInfo.score = -bankerWin
                messageHandle.game_update_currency(-bankerWin, seat.userId, room.roomNo)
                data_game_details.create_game_details(userSettleResult.userId, 2, str(room.roomNo), -bankerWin,
                                                      int(0.5 * room.score), int(time.time()))
            daerSettlePlayerInfo.totalScore = seat.score

        recSettleSingle = RecSettleSingle()
        recSettleSingle.allocId = 2
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())
        recSettleSingle.content = douniuPlayerOneSetResult.SerializeToString()
        messageHandle.broadcast_seat_to_gateway(SETTLE_GAME, recSettleSingle, room)

        record_cmd.execute(room, users[1:], scores[1:])
        room.clear()

        levelSeat = []
        for s in room.seats:
            if s.score < room.leaveScore:
                levelSeat.append(s.userId)
        for l in levelSeat:
            room.exit(l, messageHandle)
        room.gameCount += 1
        for seat in room.seats:
            t = threading.Thread(target=ready_timeout.execute,
                                 args=(room.gameCount, room.roomNo, messageHandle, seat.userId, seat.intoDate),
                                 name='ready_timeout')  # 线程对象.
            t.start()
