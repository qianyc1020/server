# coding=utf-8
import time

from protocol.base.game_base_pb2 import RecGpsInfo


class Room(object):

    def __init__(self, roomNo, count, gameRules, matchLevel):
        self.roomNo = roomNo
        self.count = count
        self.gameRules = gameRules
        self.matchLevel = matchLevel
        self.watchSeats = []
        self.seats = []
        self.seatNos = []
        for i in range(0, count):
            self.seatNos.append(i + 1)
        self.gameCount = 0
        self.startDate = int(time.time())

    def clear(self):
        for s in self.seats:
            s.clear()
        for s in self.watchSeats:
            s.clear()

    def getSeatBySeatNo(self, seatNo):
        for s in self.seats:
            if s.seatNo == seatNo:
                return s
        return None

    def getSeatByUserId(self, userId):
        for s in self.seats:
            if s.userId == userId:
                return s
        return None

    def getWatchSeatByUserId(self, userId):
        for s in self.watchSeats:
            if s.userId == userId:
                return s
        return None

    def gpsinfo(self):
        recGpsInfo = RecGpsInfo()
        for seat in self.seats:
            gpsPlayerInfo = recGpsInfo.playerInfos.add()
            gpsPlayerInfo.gpsInfo = seat.getGpsInfo()
            gpsPlayerInfo.playerId = seat.getUserId()
        return recGpsInfo
