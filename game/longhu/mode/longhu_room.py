# coding=utf-8
import base64
import time

import core.globalvar as gl
from core import config
from game.longhu.command.game import roomover_cmd
from game.longhu.mode.game_status import GameStatus
from game.longhu.mode.longhu_seat import LonghuSeat
from mode.game.position import Position
from mode.game.room import Room
from protocol.base.base_pb2 import EXECUTE_ACTION, UPDATE_GAME_INFO, UPDATE_GAME_PLAYER_INFO, SELF_INFO, BANKER_LIST, \
    WATCH_SIZE, TREND, REENTER_GAME_INFO, POSITION_SCORE, ASK_ACTION, EXIT_GAME, START_GAME
from protocol.base.game_base_pb2 import RecExecuteAction, RecUpdateGameInfo, RecUpdateGameUsers, RecReEnterGameInfo
from protocol.game.longfeng_pb2 import BaiRenLongFengBetScoreAction, BaiRenLongFengCreateRoom, ShangZhuangList, \
    BaiRenLongFengWatchSize, BaiRenLongFengTrend, BaiRenLongFengPositions, BaiRenLongFengRecAsk, BankerConfirm


class LonghuRoom(Room):

    def __init__(self, roomNo=0, count=0, gameRules=0, matchLevel=0, score=0, inScore=0, leaveScore=0):
        super(LonghuRoom, self).__init__(roomNo, count, gameRules, matchLevel)
        self.score = score
        self.inScore = inScore
        self.leaveScore = leaveScore
        self.gameStatus = GameStatus.WAITING
        self.banker = 1
        self.bankerScore = 0
        self.historyActions = []
        self.positions = []
        self.positions.append(Position())
        self.positions.append(Position())
        self.positions.append(Position())
        self.bankerList = []
        self.xiazhuang = False
        self.started = False
        self.dayingjia = 0
        self.trend = []
        self.betScores = []
        self.shensuanziPlayIndex = -1

    def object_to_dict(self, d):
        if "seats" in d:
            seat = []
            for s in d["seats"]:
                s1 = LonghuSeat()
                s1.__dict__ = eval(s)
                seat.append(s1)
            d["seats"] = seat

        if "watchSeats" in d:
            watchSeats = []
            for s in d["watchSeats"]:
                s1 = LonghuSeat()
                s1.__dict__ = eval(s)
                watchSeats.append(s1)
            d["watchSeats"] = watchSeats

        if "positions" in d:
            positions = []
            for s in d["positions"]:
                s1 = Position()
                s1.__dict__ = eval(s)
                positions.append(s1)
            d["positions"] = positions

        if "historyActions" in d:
            historyActions = []
            for s in d["historyActions"]:
                historyActions.append(base64.b64decode(s))
            d["historyActions"] = historyActions

        if "betScores" in d:
            betScores = []
            for s in d["betScores"]:
                betScores.append(base64.b64decode(s))
            d["betScores"] = betScores
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
        positions = []
        for s in self.positions:
            positions.append(str(s.__dict__))
        dict["positions"] = positions
        historyActions = []
        for s in self.historyActions:
            historyActions.append(base64.b64encode(s))
        dict["historyActions"] = historyActions

        betScores = []
        for b in self.betScores:
            betScores.append(base64.b64encode(b))
        dict["betScores"] = betScores
        return str(dict)

    def clear(self):
        super(LonghuRoom, self).clear()
        self.gameStatus = GameStatus.WAITING
        self.started = False
        self.historyActions = []
        for p in self.positions:
            p.clear()
        self.shensuanziPlayIndex = -1

    def bankerConfirm(self, messageHandle):
        if 1 != self.banker:
            seat = self.getWatchSeatByUserId(self.banker)
            if seat is None or self.bankerScore < int(config.get("longhu", "getBankerScore")):
                self.banker = 1
        if self.xiazhuang or 1 == self.banker:
            self.xiazhuang = False
            # TODO 排序
            while len(self.bankerList) > 0:
                bankerId = self.bankerList[0]
                self.bankerList.remove(bankerId)
                bankerSeat = self.getWatchSeatByUserId(bankerId)
                if bankerSeat is not None and bankerSeat.score >= bankerSeat.shangzhuangScore >= int(
                        config.get("longhu", "getBankerScore")):
                    self.banker = bankerId
                    break

        bankerConfirm = BankerConfirm()
        userInfo = bankerConfirm.banker
        if 1 == self.banker:
            if bool(config.get("longhu", "onlyPlayerBanker")):
                self.updateBankerList(messageHandle, 0)
                return
            userInfo.playerId = 1
            userInfo.score = int(config.get("longhu", "bankerDefaultScore"))
            userInfo.online = True
            self.bankerScore = int(config.get("longhu", "bankerDefaultScore"))
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
        self.started = True
        self.startDate = time.time()
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
        if 2 != actionType:
            self.historyActions.append(recExecuteAction.SerializeToString())

    def sendBetScore(self, messageHandle):
        if 0 < len(self.betScores):
            action = BaiRenLongFengBetScoreAction()
            for b in self.betScores:
                a = action.betScore.add()
                a.ParseFromString(b)
            self.betScores = []
            executeAction = RecExecuteAction()
            executeAction.actionType = 2
            executeAction.data = action.SerializeToString()
            messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, self)

    def recUpdateGameInfo(self, messageHandle):
        recUpdateGameInfo = RecUpdateGameInfo()
        recUpdateGameInfo.allocId = 8
        tuitongziCreateRoom = BaiRenLongFengCreateRoom()
        tuitongziCreateRoom.baseScore = self.score
        tuitongziCreateRoom.inScore = self.inScore
        tuitongziCreateRoom.leaveScore = self.leaveScore
        recUpdateGameInfo.content = tuitongziCreateRoom.SerializeToString()
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
        watchSize = BaiRenLongFengWatchSize()
        watchSize.watchSize = len(self.watchSeats)
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(WATCH_SIZE, watchSize, self)
        else:
            messageHandle.send_to_gateway(WATCH_SIZE, watchSize)

    def updateTrend(self, messageHandle, userId):
        baiRenTuiTongZiTrend = BaiRenLongFengTrend()
        for t in self.trend:
            sigleTrend = baiRenTuiTongZiTrend.trends.add()
            sigleTrend.positionWin.extend(t)
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(TREND, baiRenTuiTongZiTrend, self)
        else:
            messageHandle.send_to_gateway(TREND, baiRenTuiTongZiTrend)

    def recReEnterGameInfo(self, messageHandle, userId):
        recReEnterGameInfo = RecReEnterGameInfo()
        recReEnterGameInfo.allocId = 8
        for a in self.historyActions:
            executeAction = recReEnterGameInfo.actionInfos.add()
            executeAction.ParseFromString(a)
        messageHandle.send_to_gateway(REENTER_GAME_INFO, recReEnterGameInfo, userId)

        positions = BaiRenLongFengPositions()
        for i in range(0, len(self.positions)):
            action = positions.positions.add()
            action.index = i
            action.score = self.positions[i].totalScore
        positions.shensuanziPositions = self.shensuanziPlayIndex
        messageHandle.send_to_gateway(POSITION_SCORE, positions)

    def executeAsk(self, messageHandle, userId, type):
        if GameStatus.PLAYING != self.gameStatus and 2 == type:
            return
        if GameStatus.PLAYING == self.gameStatus and 1 == type:
            return
        tuitongziRecAsk = BaiRenLongFengRecAsk()
        tuitongziRecAsk.time = int((9500 - time.time() + self.startDate) / 1000)
        if 2 == type:
            tuitongziRecAsk.time = int((11500 - time.time() + self.startDate) / 1000)
        tuitongziRecAsk.type = type
        if 0 == userId:
            messageHandle.broadcast_watch_to_gateway(ASK_ACTION, tuitongziRecAsk, self)
        else:
            messageHandle.send_to_gateway(ASK_ACTION, tuitongziRecAsk)

    def exit(self, userId, messageHandle):
        seat = self.getWatchSeatByUserId(userId)
        if seat is not None:
            if seat.playScore != 0 or (self.banker == seat.userId and self.started):
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
            messageHandle.send_to_gateway(EXIT_GAME, None)
            if inseat:
                self.recUpdateScore(messageHandle, 0)
            self.updateWatchSize(messageHandle, 0)
            if 0 == len(self.watchSeats):
                roomover_cmd.execute(self, messageHandle)
