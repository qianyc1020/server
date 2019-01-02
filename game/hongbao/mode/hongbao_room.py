# coding=utf-8
import random
import threading
import time

import core.globalvar as gl
from core import config
from game.hongbao.command.game import roomover_cmd
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.timeout import qiang_timeout
from mode.game.room import Room
from protocol.base.base_pb2 import EXECUTE_ACTION, UPDATE_GAME_INFO, UPDATE_GAME_PLAYER_INFO, SELF_INFO, BANKER_LIST, \
    WATCH_SIZE, REENTER_GAME_INFO, ASK_ACTION, EXIT_GAME, START_GAME
from protocol.base.game_base_pb2 import RecExecuteAction, RecUpdateGameInfo, RecUpdateGameUsers, RecReEnterGameInfo
from protocol.base.server_to_game_pb2 import UserExit
from protocol.game.bairen_pb2 import BaiRenCreateRoom, ShangZhuangList, \
    BaiRenWatchSize, BaiRenRecAsk, BankerConfirm
from protocol.game.hongbao_pb2 import BaiRenHongbaoScore


class HongbaoRoom(Room):

    def __init__(self, roomNo=0, count=0, gameRules=0, matchLevel=0, score=0, inScore=0, leaveScore=0):
        super(HongbaoRoom, self).__init__(roomNo, count, gameRules, matchLevel)
        self.score = score
        self.inScore = inScore
        self.leaveScore = leaveScore
        self.gameStatus = GameStatus.WAITING
        self.banker = 1
        self.bankerScore = 0
        self.historyActions = []
        self.bankerList = []
        self.xiazhuang = False
        self.started = False
        self.userScore = {}
        self.selectNum = -1
        self.hongbaolist = []

    def save(self, redis):
        if self.gameStatus != GameStatus.DESTORY:
            redis.setobj("room_" + str(self.roomNo), self)

    def clear(self):
        super(HongbaoRoom, self).clear()
        self.gameStatus = GameStatus.WAITING
        self.started = False
        self.historyActions = []
        self.userScore = {}
        self.selectNum = -1
        self.hongbaolist = []

    def bankerConfirm(self, messageHandle):
        if 1 != self.banker:
            seat = self.getWatchSeatByUserId(self.banker)
            if seat is None or self.bankerScore < int(config.get("hongbao", "getBankerScore")):
                self.banker = 1
        if self.xiazhuang or 1 == self.banker:
            self.banker = 1
            self.xiazhuang = False
            while len(self.bankerList) > 0:
                bankerId = self.bankerList[0]
                self.bankerList.remove(bankerId)
                bankerSeat = self.getWatchSeatByUserId(bankerId)
                if bankerSeat is not None and bankerSeat.score >= bankerSeat.shangzhuangScore >= int(
                        config.get("hongbao", "getBankerScore")):
                    self.banker = bankerId
                    break

        bankerConfirm = BankerConfirm()
        userInfo = bankerConfirm.banker
        if 1 == self.banker:
            if config.get("hongbao", "onlyPlayerBanker") == "True":
                self.updateBankerList(messageHandle, 0)
                return
            userInfo.playerId = 0
            userInfo.nick = '系统小乐'
            userInfo.score = int(config.get("hongbao", "bankerDefaultScore"))
            userInfo.online = True
            self.bankerScore = int(config.get("hongbao", "bankerDefaultScore"))
        else:
            s = self.getWatchSeatByUserId(self.banker)
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
            userInfo.loc = 0
            userInfo.consumeVip = s.level
            self.bankerScore = s.shangzhuangScore
        messageHandle.broadcast_watch_to_gateway(START_GAME, None, self)
        self.startDate = int(time.time())
        bankerConfirm.shangzhuangScore = self.bankerScore
        self.executeAction(0, 4, bankerConfirm, messageHandle)
        self.updateBankerList(messageHandle, 0)

    def executeAction(self, userId, actionType, data, messageHandle):
        recExecuteAction = RecExecuteAction()
        recExecuteAction.actionType = actionType
        recExecuteAction.playerId = userId
        if data is not None:
            recExecuteAction.data = data.SerializeToString()
        messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, recExecuteAction, self)
        self.historyActions.append(recExecuteAction.SerializeToString())

    def recUpdateGameInfo(self, messageHandle):
        recUpdateGameInfo = RecUpdateGameInfo()
        recUpdateGameInfo.allocId = 11
        hongbaoCreateRoom = BaiRenCreateRoom()
        hongbaoCreateRoom.baseScore = self.score
        hongbaoCreateRoom.inScore = self.inScore
        hongbaoCreateRoom.leaveScore = self.leaveScore
        recUpdateGameInfo.content = hongbaoCreateRoom.SerializeToString()
        messageHandle.send_to_gateway(UPDATE_GAME_INFO, recUpdateGameInfo)

    def recUpdateScore(self, messageHandle, userId):
        recUpdateGameUsers = RecUpdateGameUsers()
        i = 1
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
            userInfo.loc = i
            userInfo.consumeVip = s.level
            i += 1
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(UPDATE_GAME_PLAYER_INFO, recUpdateGameUsers, self)
        else:
            messageHandle.send_to_gateway(UPDATE_GAME_PLAYER_INFO, recUpdateGameUsers)
            s = self.getWatchSeatByUserId(userId)
            userInfo = RecUpdateGameUsers.UserInfo()
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
            userInfo.loc = i
            userInfo.consumeVip = s.level
            messageHandle.send_to_gateway(SELF_INFO, userInfo)

    def updateBankerList(self, messageHandle, userId):
        shangZhuangList = ShangZhuangList()
        for b in self.bankerList:
            s = self.getWatchSeatByUserId(b)
            if s is not None:
                bankerConfirm = shangZhuangList.bankerList.add()
                userInfo = bankerConfirm.banker
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
                userInfo.consumeVip = s.level
                bankerConfirm.shangzhuangScore = s.shangzhuangScore
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(BANKER_LIST, shangZhuangList, self)
        else:
            messageHandle.send_to_gateway(BANKER_LIST, shangZhuangList)

    def updateWatchSize(self, messageHandle, userId):
        watchSize = BaiRenWatchSize()
        watchSize.watchSize = len(self.watchSeats)
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(WATCH_SIZE, watchSize, self)
        else:
            messageHandle.send_to_gateway(WATCH_SIZE, watchSize)

    def recReEnterGameInfo(self, messageHandle, userId):
        recReEnterGameInfo = RecReEnterGameInfo()
        recReEnterGameInfo.allocId = 11
        for a in self.historyActions:
            executeAction = recReEnterGameInfo.actionInfos.add()
            executeAction.ParseFromString(a)
        messageHandle.send_to_gateway(REENTER_GAME_INFO, recReEnterGameInfo, userId)

    def executeAsk(self, messageHandle, userId, type):
        if GameStatus.PLAYING != self.gameStatus and 2 == type:
            return
        if self.started and 1 == type:
            return
        hongbaoRecAsk = BaiRenRecAsk()
        hongbaoRecAsk.time = int(3.5 - time.time() + self.startDate)
        if 2 == type:
            hongbaoRecAsk.time = int(8.5 - time.time() + self.startDate)
        hongbaoRecAsk.type = type
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(ASK_ACTION, hongbaoRecAsk, self)
        else:
            messageHandle.send_to_gateway(ASK_ACTION, hongbaoRecAsk, userId)

    def bankerSelectNum(self, num, messageHandle):
        selectNum = BaiRenHongbaoScore()
        selectNum.score = num
        self.executeAction(self.banker, 1, selectNum, messageHandle)
        self.selectNum = num
        self.started = True
        self.startDate = int(time.time())
        self.executeAsk(messageHandle, 0, 2)

        threading.Thread(target=qiang_timeout.execute, args=(self.roomNo, self.gameCount, messageHandle,),
                         name='qiang_timeout').start()  # 线程对象.
        hongbaolist = []
        zonge = self.bankerScore - 10
        for i in range(0, 10):
            hongbaolist.append(1)
        while 0 != zonge:
            r = int(random.random() * zonge / 10)
            hongbaolist[random.randint(0, 9)] += r
            zonge -= r
            if 10 >= zonge:
                hongbaolist[random.randint(0, 9)] += zonge
                zonge = 0
        random.shuffle(hongbaolist)
        self.hongbaolist = hongbaolist

    def exit(self, userId, messageHandle):
        seat = self.getWatchSeatByUserId(userId)
        if seat is not None:
            if userId in self.userScore or (self.banker == seat.userId and self.gameStatus == GameStatus.PLAYING):
                return
            if userId == self.banker:
                self.xiazhuang = True
            inseat = False
            while seat is not None:
                self.watchSeats.remove(seat)
                seat = self.getWatchSeatByUserId(userId)
            seat = self.getSeatByUserId(userId)
            while seat is not None:
                inseat = True
                self.seats.remove(seat)
                seat = self.getSeatByUserId(userId)
            if userId in self.bankerList:
                self.bankerList.remove(userId)
                self.updateBankerList(messageHandle, 0)
            redis = gl.get_v("redis")
            redis.delobj(str(userId) + "_room")
            userExit = UserExit()
            userExit.playerId = userId
            from game.hongbao.server.server import Server
            Server.send_to_coordinate(EXIT_GAME, userExit)
            if inseat:
                self.recUpdateScore(messageHandle, 0)
            self.updateWatchSize(messageHandle, 0)
            if 0 == len(self.watchSeats):
                roomover_cmd.execute(self, messageHandle)
