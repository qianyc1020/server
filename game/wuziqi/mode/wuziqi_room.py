# coding=utf-8
import base64

import core.globalvar as gl
from game.wuziqi.command.game import roomover_cmd
from game.wuziqi.mode.game_status import GameStatus
from game.wuziqi.mode.wuziqi_seat import WuziqiSeat
from mode.game.room import Room
from protocol.base.base_pb2 import EXECUTE_ACTION, UPDATE_GAME_INFO, UPDATE_GAME_PLAYER_INFO, \
    REENTER_GAME_INFO, EXIT_GAME
from protocol.base.game_base_pb2 import RecExecuteAction, RecUpdateGameInfo, RecUpdateGameUsers, RecReEnterGameInfo
from protocol.base.server_to_game_pb2 import UserExit
from protocol.game.wuziqi_pb2 import WuziqiCreateRoom


class WuziqiRoom(Room):

    def __init__(self, roomNo=0, count=2, gameRules=0, matchLevel=0, score=0):
        super(WuziqiRoom, self).__init__(roomNo, count, gameRules, matchLevel)
        self.score = score
        self.gameStatus = GameStatus.WAITING
        self.banker = 1
        self.historyActions = []
        self.operationSeatNo = 0

    def object_to_dict(self, d):
        if "seats" in d:
            seat = []
            for s in d["seats"]:
                s1 = WuziqiSeat()
                s1.__dict__ = eval(s)
                seat.append(s1)
            d["seats"] = seat

        if "watchSeats" in d:
            watchSeats = []
            for s in d["watchSeats"]:
                s1 = WuziqiSeat()
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
        super(WuziqiRoom, self).clear()
        self.gameStatus = GameStatus.WAITING
        self.started = False
        self.historyActions = []
        self.userScore = {}
        self.selectNum = -1
        self.wuziqilist = []

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
        recUpdateGameInfo.allocId = 3
        wuziqiCreateRoom = WuziqiCreateRoom()
        wuziqiCreateRoom.countDown = 10
        recUpdateGameInfo.content = wuziqiCreateRoom.SerializeToString()
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
            userInfo.banker = 1 == s.seatNo
        if 0 == userId:
            messageHandle.broadcast_seat_to_gateway(UPDATE_GAME_PLAYER_INFO, recUpdateGameUsers, self)
        else:
            messageHandle.send_to_gateway(UPDATE_GAME_PLAYER_INFO, recUpdateGameUsers)

    def recReEnterGameInfo(self, messageHandle, userId):
        recReEnterGameInfo = RecReEnterGameInfo()
        recReEnterGameInfo.allocId = 3
        for a in self.historyActions:
            executeAction = recReEnterGameInfo.actionInfos.add()
            executeAction.ParseFromString(a)
        messageHandle.send_to_gateway(REENTER_GAME_INFO, recReEnterGameInfo, userId)

    def exit(self, userId, messageHandle):
        if self.gameStatus != GameStatus.PLAYING:

            seat = self.getSeatByUserId(userId)
            if seat is not None:
                while seat is not None:
                    self.seatNos.append(seat.seatNo)
                    self.seats.remove(seat)
                    seat = self.getSeatByUserId(userId)
                redis = gl.get_v("redis")
                redis.delobj(str(userId) + "_room")
                userExit = UserExit()
                userExit.playerId = userId
                from game.wuziqi.server.server import Server
                Server.send_to_coordinate(EXIT_GAME, userExit)
                if 0 == len(self.seats):
                    roomover_cmd.execute(self, messageHandle)
