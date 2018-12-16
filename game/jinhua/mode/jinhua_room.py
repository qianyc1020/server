# coding=utf-8
import random
import threading
import time

import grpc

import core.globalvar as gl
from game.jinhua.command.game import roomover_cmd, gamestart_cmd, gameover_cmd
from game.jinhua.mode.game_status import GameStatus
from game.jinhua.timeout import play_timeout
from mode.game.room import Room
from protocol.base.base_pb2 import EXECUTE_ACTION, UPDATE_GAME_INFO, UPDATE_GAME_PLAYER_INFO, \
    REENTER_GAME_INFO, ASK_ACTION, EXIT_GAME, ROUND_ACTION, APPLY_CHANGE_MATCH
from protocol.base.game_base_pb2 import RecExecuteAction, RecUpdateGameInfo, RecUpdateGameUsers, RecReEnterGameInfo
from protocol.base.server_to_game_pb2 import UserExit
from protocol.game import zhipai_pb2_grpc
from protocol.game.bairen_pb2 import BaiRenRecAsk
from protocol.game.jinhua_pb2 import JinhuaRecRound, JinhuaBankerConfirm, JinhuaCreateRoom
from protocol.game.zhipai_pb2 import SettleData


class JinhuaRoom(Room):

    def __init__(self, roomNo=0, count=0, gameRules=0, matchLevel=0, score=0, inScore=0, leaveScore=0, gameType=0):
        super(JinhuaRoom, self).__init__(roomNo, count, gameRules, matchLevel)
        self.score = score
        self.inScore = inScore
        self.leaveScore = leaveScore
        self.gameStatus = GameStatus.WAITING
        self.banker = 0
        self.deskScore = 0
        self.minScore = 0
        self.operationSeat = 0
        self.gameType = gameType
        self.operationTime = 0
        self.historyActions = []

    def save(self, redis):
        if self.gameStatus != GameStatus.DESTORY:
            redis.setobj("room_" + str(self.roomNo), self)

    def clear(self):
        super(JinhuaRoom, self).clear()
        self.gameStatus = GameStatus.WAITING
        self.historyActions = []
        self.operationSeat = 0
        self.minScore = 0
        self.deskScore = 0

    def bankerConfirm(self, messageHandle):
        bankerSeat = self.getSeatByUserId(self.banker)
        if bankerSeat == None:
            bankerSeat = self.seats[random.randint(0, len(self.seats)) - 1]
            self.banker = bankerSeat.userId
        bankerConfirm = JinhuaBankerConfirm()
        bankerConfirm.bankerId = self.banker
        self.executeAction(0, 4, bankerConfirm, messageHandle)
        self.operationSeat = bankerSeat.seatNo
        self.changeOperation()

    def getNextSeat(self, next):
        if 5 == next:
            next = 1
        else:
            next += 1
        return next

    def changeOperation(self):
        nextOpeartion = self.getNextSeat(self.operationSeat)
        nextOpeartionSeat = self.getSeatBySeatNo(nextOpeartion)
        count = 0
        while None == nextOpeartionSeat or nextOpeartionSeat.end or nextOpeartionSeat.guanzhan:
            nextOpeartion = self.getNextSeat(nextOpeartion)
            nextOpeartionSeat = self.getSeatBySeatNo(nextOpeartion)
            count += 1
            if count == self.count:
                return
        self.operationSeat = nextOpeartion

    def executeAction(self, userId, actionType, data, messageHandle):
        recExecuteAction = RecExecuteAction()
        recExecuteAction.actionType = actionType
        recExecuteAction.playerId = userId
        if data is not None:
            recExecuteAction.data = data.SerializeToString()
        messageHandle.broadcast_seat_to_gateway(EXECUTE_ACTION, recExecuteAction, self)
        if 2 != actionType:
            self.historyActions.append(recExecuteAction.SerializeToString())

    def recUpdateGameInfo(self, messageHandle):
        recUpdateGameInfo = RecUpdateGameInfo()
        recUpdateGameInfo.allocId = 1
        jinhuaCreateRoom = JinhuaCreateRoom()
        jinhuaCreateRoom.baseScore = self.score
        jinhuaCreateRoom.inScore = self.inScore
        jinhuaCreateRoom.leaveScore = self.leaveScore
        jinhuaCreateRoom.gameType = self.gameType
        jinhuaCreateRoom.gameRules = self.gameRules
        jinhuaCreateRoom.match = True
        recUpdateGameInfo.content = jinhuaCreateRoom.SerializeToString()
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
            userInfo.score = s.score - s.playScore
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
        recReEnterGameInfo.allocId = 1
        for a in self.historyActions:
            executeAction = recReEnterGameInfo.actionInfos.add()
            executeAction.ParseFromString(a)
        messageHandle.send_to_gateway(REENTER_GAME_INFO, recReEnterGameInfo, userId)
        if self.gameStatus == GameStatus.PLAYING:
            self.executeRound(messageHandle, userId)

    def executeRound(self, messageHandle, userId):

        operation = self.getSeatBySeatNo(self.operationSeat)
        roundAction = JinhuaRecRound()
        roundAction.randId = int(time.time())
        roundAction.playerId = operation.userId
        roundAction.minScore = self.minScore
        if 0 == userId:
            self.operationTime = int(time.time())
            roundAction.actionTime = 60

            t = threading.Thread(target=play_timeout.execute,
                                 args=(self.roomNo, messageHandle, operation.userId, self.gameCount, operation.round),
                                 name='play_timeout')  # 线程对象.
            t.start()
            messageHandle.broadcast_seat_to_gateway(ROUND_ACTION, roundAction, self)
        else:
            roundAction.actionTime = 60 - int(time.time()) + self.operationTime
            messageHandle.send_to_gateway(ROUND_ACTION, roundAction, userId)

    def executeAsk(self, messageHandle, userId, type):
        if GameStatus.PLAYING != self.gameStatus and 2 == type:
            return
        if GameStatus.PLAYING == self.gameStatus and 1 == type:
            return
        jinhuaRecAsk = BaiRenRecAsk()
        jinhuaRecAsk.time = int(19.5 - time.time() + self.startDate)
        if 1 == type:
            jinhuaRecAsk.time = int(9.5 - time.time() + self.startDate)
        jinhuaRecAsk.type = type
        if 0 == userId:
            messageHandle.broadcast_seat_to_gateway(ASK_ACTION, jinhuaRecAsk, self)
        else:
            messageHandle.send_to_gateway(ASK_ACTION, jinhuaRecAsk, userId)

    def exit(self, userId, messageHandle):
        self.exitOrChangeMatch(userId, messageHandle, False)

    def changeMatch(self, userId, messageHandle):
        self.exitOrChangeMatch(userId, messageHandle, True)

    def exitOrChangeMatch(self, userId, messageHandle, changeMatch):
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
            userExit.roomNo = self.roomNo
            userExit.level = self.matchLevel
            from game.jinhua.server.server import Server
            Server.send_to_coordinate(APPLY_CHANGE_MATCH if changeMatch else EXIT_GAME, userExit)
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

    def playScore(self, seat, betScoreAction, messageHandle):
        seat.playScore += betScoreAction.score
        self.deskScore += betScoreAction.score
        self.minScore = betScoreAction.score / 2 if seat.lookCard else betScoreAction.score
        self.executeAction(seat.userId, 2, betScoreAction, messageHandle)
        self.changeOperation()
        self.executeRound(messageHandle, 0)
        seat.round += 1
        self.checkRound(messageHandle)

    def abandon(self, messageHandle, seat):
        self.settle(seat, seat)
        seat.end = True
        self.executeAction(seat.userId, 1, None, messageHandle)
        if not self.checkOver(messageHandle) and seat.seatNo == self.operationSeat:
            self.changeOperation()
            self.executeRound(messageHandle, 0)
            seat.round += 1
            self.checkRound(messageHandle)

    def checkRound(self, messageHandle):
        notend = []
        for seat in self.seats:
            if not seat.end and not seat.guanzhan:
                if seat.round != 20:
                    return
                notend.append(seat)
        if len(notend) > 1:
            self.allCompare(notend, messageHandle)

    def allCompare(self, notend, messageHandle):
        wins = []
        wins.append(notend[0])
        for i in range(1, len(notend)):
            settleResult = self.settle(wins[0], notend[i])
            if settleResult.userSettleResule[0].win > 0:
                notend[i].end = True
            elif settleResult.userSettleResule[0].win < 0:
                for w in wins:
                    w.end = True
                wins = []
                wins.append(notend[i])
            else:
                wins.append(notend[i])
        for seat in self.seats:
            for n in notend:
                if n != seat:
                    seat.canLookUser.append(n.userId)
        self.executeAction(0, 5, None, messageHandle)
        gameover_cmd.execute(self, messageHandle, wins)

    def checkOver(self, messageHandle):
        win = None
        for seat in self.seats:
            if not seat.end and not seat.guanzhan:
                if win is None:
                    win = seat
                else:
                    return False
        if win is not None:
            self.settle(win, win)
            wins = [win]
            gameover_cmd.execute(self, messageHandle, wins)
            return True
        return False

    def settle(self, seat, compareSeat):
        settleData = SettleData()
        userSettleData = settleData.userSettleData.add()
        userSettleData.userId = seat.userId
        userSettleData.cardlist.extend(seat.initialCards)

        userSettleData = settleData.userSettleData.add()
        userSettleData.userId = compareSeat.userId
        userSettleData.cardlist.extend(compareSeat.initialCards)

        conn = grpc.insecure_channel('127.0.0.1:50001')
        client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
        settleResult = client.settle(settleData)

        seat.cardType = settleResult.userSettleResule[0].cardValue
        compareSeat.cardType = settleResult.userSettleResule[1].cardValue

        return settleResult
