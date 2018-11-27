# coding=utf-8
import base64
import threading

import random

import core.globalvar as gl
from game.douniu.command.game import roomover_cmd, gamestart_cmd, gameover_cmd, dealcard_cmd
from game.douniu.mode.game_status import GameStatus
from game.douniu.mode.douniu_seat import DouniuSeat
from game.douniu.timeout import operation_timeout
from mode.game.room import Room
from protocol.base.base_pb2 import EXECUTE_ACTION, UPDATE_GAME_INFO, UPDATE_GAME_PLAYER_INFO, \
    REENTER_GAME_INFO, ASK_ACTION, EXIT_GAME
from protocol.base.game_base_pb2 import RecExecuteAction, RecUpdateGameInfo, RecUpdateGameUsers, RecReEnterGameInfo
from protocol.base.server_to_game_pb2 import UserExit
from protocol.game.bairen_pb2 import BaiRenRecAsk
from protocol.game.douniu_pb2 import DouniuBankerConfirm, DouniuCreateRoom, DouniuCardAction


class DouniuRoom(Room):

    def __init__(self, roomNo=0, count=0, gameRules=0, matchLevel=0, score=0, inScore=0, leaveScore=0, gameType=0,
                 betType=1):
        super(DouniuRoom, self).__init__(roomNo, count, gameRules, matchLevel)
        self.score = score
        self.inScore = inScore
        self.leaveScore = leaveScore
        self.gameStatus = GameStatus.WAITING
        self.banker = 0
        self.gameType = gameType
        self.betType = betType
        self.historyActions = []

    def object_to_dict(self, d):
        if "seats" in d:
            seat = []
            for s in d["seats"]:
                s1 = DouniuSeat()
                s1.__dict__ = eval(s)
                seat.append(s1)
            d["seats"] = seat

        if "watchSeats" in d:
            watchSeats = []
            for s in d["watchSeats"]:
                s1 = DouniuSeat()
                s1.__dict__ = eval(s)
                watchSeats.append(s1)
            d["watchSeats"] = watchSeats

        if "historyActions" in d:
            historyActions = []
            for s in d["historyActions"]:
                historyActions.append(base64.b64decode(s))
            d["historyActions"] = historyActions

        return d

    def dict_to_object(self):
        d = self.__dict__
        dict = d.copy()
        seats = []
        for s in self.seats:
            seats.append(str(s.__dict__))
        dict["seats"] = seats
        watchSeats = []
        for s in self.watchSeats:
            watchSeats.append(str(s.__dict__))
        dict["watchSeats"] = watchSeats
        historyActions = []
        for s in self.historyActions:
            historyActions.append(base64.b64encode(s))
        dict["historyActions"] = historyActions
        return str(dict)

    def clear(self):
        super(DouniuRoom, self).clear()
        self.gameStatus = GameStatus.WAITING
        self.historyActions = []
        self.banker = 0

    def bankerConfirm(self, messageHandle):
        bankerConfirm = DouniuBankerConfirm()
        bankerConfirm.bankerId = self.banker
        self.executeAction(0, 4, bankerConfirm, messageHandle)

    def executeAction(self, userId, actionType, data, messageHandle):
        recExecuteAction = RecExecuteAction()
        recExecuteAction.actionType = actionType
        recExecuteAction.playerId = userId
        if data is not None:
            recExecuteAction.data = data.SerializeToString()
        messageHandle.broadcast_seat_to_gateway(EXECUTE_ACTION, recExecuteAction, self)
        self.historyActions.append(recExecuteAction.SerializeToString())

    def recUpdateGameInfo(self, messageHandle):
        recUpdateGameInfo = RecUpdateGameInfo()
        recUpdateGameInfo.allocId = 2
        douniuCreateRoom = DouniuCreateRoom()
        douniuCreateRoom.baseScore = self.score
        douniuCreateRoom.inScore = self.inScore
        douniuCreateRoom.leaveScore = self.leaveScore
        douniuCreateRoom.type = self.gameType
        douniuCreateRoom.gameRules = self.gameRules
        douniuCreateRoom.betType = self.betType
        recUpdateGameInfo.content = douniuCreateRoom.SerializeToString()
        messageHandle.send_to_gateway(UPDATE_GAME_INFO, recUpdateGameInfo)

    def recUpdateScore(self, messageHandle, userId):
        recUpdateGameUsers = RecUpdateGameUsers()
        for s in self.seats:
            userInfo = recUpdateGameUsers.users.add()
            userInfo.account = s.account
            userInfo.playerId = s.userId
            userInfo.headUrl = s.head
            userInfo.createTime = s.createDate
            userInfo.ip = s.ip
            userInfo.online = s.online
            userInfo.nick = s.nickname
            userInfo.ready = s.ready
            userInfo.score = s.score
            userInfo.sex = s.sex
            userInfo.totalCount = s.total_count
            userInfo.loc = s.seatNo
            userInfo.consumeVip = s.level
        if 0 == userId:
            messageHandle.broadcast_seat_to_gateway(UPDATE_GAME_PLAYER_INFO, recUpdateGameUsers, self)
        else:
            messageHandle.send_to_gateway(UPDATE_GAME_PLAYER_INFO, recUpdateGameUsers)

    def recReEnterGameInfo(self, messageHandle, userId):
        recReEnterGameInfo = RecReEnterGameInfo()
        recReEnterGameInfo.allocId = 2
        seat = self.getSeatByUserId(userId)
        for a in self.historyActions:
            executeAction = recReEnterGameInfo.actionInfos.add()
            executeAction.ParseFromString(a)
            if 0 == executeAction.actionType:
                dealCardAction = DouniuCardAction()
                dealCardAction.ParseFromString(executeAction.data)
                if 4 == len(dealCardAction.cards):
                    if 0 != len(seat.initialCards):
                        dealCardAction = DouniuCardAction()
                        dealCardAction.cards.extend(seat.initialCards)
                    else:
                        dealCardAction = DouniuCardAction()
                        dealCardAction.cards.extend([0, 0, 0, 0])
                else:
                    if 0 != len(seat.initialCards):
                        dealCardAction = DouniuCardAction()
                        dealCardAction.cards.append(seat.initialCards[4])
                    else:
                        dealCardAction = DouniuCardAction()
                        dealCardAction.cards.append(0)
                executeAction.data = dealCardAction.SerializeToString()
        messageHandle.send_to_gateway(REENTER_GAME_INFO, recReEnterGameInfo, userId)
        if self.gameStatus == GameStatus.GRABING:
            self.executeAsk(messageHandle, userId, 1)
        if self.gameStatus == GameStatus.PLAYING:
            self.executeAsk(messageHandle, userId, 2)
        if self.gameStatus == GameStatus.OPENING:
            self.executeAsk(messageHandle, userId, 3)

    def executeAsk(self, messageHandle, userId, type):
        douniuRecAsk = BaiRenRecAsk()
        douniuRecAsk.type = type

        t = threading.Thread(target=operation_timeout.execute,
                             args=(self.roomNo, messageHandle, self.gameStatus, self.gameCount),
                             name='operation_timeout')  # 线程对象.
        t.start()
        if 0 == userId:
            messageHandle.broadcast_seat_to_gateway(ASK_ACTION, douniuRecAsk, self)
        else:
            messageHandle.send_to_gateway(ASK_ACTION, douniuRecAsk)

    def exit(self, userId, messageHandle):
        seat = self.getSeatByUserId(userId)
        if seat is not None and (seat.guanzhan or self.gameStatus == GameStatus.WAITING):
            while seat is not None:
                self.seatNos.append(seat.seatNo)
                self.seats.remove(seat)
                seat = self.getSeatByUserId(userId)
            redis = gl.get_v("redis")
            redis.delobj(str(userId) + "_room")
            userExit = UserExit()
            userExit.playerId = userId
            from game.douniu.server.server import Server
            Server.send_to_coordinate(EXIT_GAME, userExit)
            self.recUpdateScore(messageHandle, 0)
            if 0 == len(self.seats):
                roomover_cmd.execute(self, messageHandle)
            elif self.gameStatus == GameStatus.WAITING:
                self.checkReady(messageHandle)

    def checkReady(self, messageHandle):
        allReady = True
        for seat in self.seats:
            if not seat.ready:
                allReady = False
                break
        if allReady and len(self.seats) > 1:
            gamestart_cmd.execute(self, messageHandle)

    def checkGrab(self, messageHandle):
        bankers = []
        maxGrab = 0
        for seat in self.seats:
            if -1 == seat.grab and not seat.guanzhan:
                return
            if seat.grab > maxGrab:
                bankers = []
                bankers.append(seat.userId)
                maxGrab = seat.grab
            elif seat.grab == maxGrab:
                bankers.append(seat.userId)
        if len(bankers) > 0:
            self.banker = bankers[random.randint(0, len(bankers) - 1)]
        else:
            self.banker = self.seats[random.randint(0, len(self.seats) - 1)].userId
        self.bankerConfirm(messageHandle)
        self.gameStatus = GameStatus.PLAYING
        self.executeAsk(messageHandle, 0, 2)

    def checkPlay(self, messageHandle):
        if self.gameStatus != GameStatus.PLAYING:
            return
        for seat in self.seats:
            if -1 == seat.playScore and not seat.guanzhan and seat.userId != self.banker:
                return
        dealcard_cmd.execute(self, messageHandle)

    def checkOpen(self, messageHandle):
        for seat in self.seats:
            if not seat.openCard and not seat.guanzhan:
                return
        gameover_cmd.execute(self, messageHandle)
