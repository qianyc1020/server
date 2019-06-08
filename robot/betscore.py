# coding=utf-8
import random
import time

from protocol.base.base_pb2 import *
from protocol.base.game_base_pb2 import ReqSendAction
from protocol.game.bairen_pb2 import BaiRenBetScoreAction


class BetScore(object):

    def __init__(self, client):
        self.client = client
        self.status = True
        self.count = 0
        self.index = random.randint(1, 3)
        rs = random.randint(1, 99)
        self.score = 100
        if rs > 70:
            self.score = 1000
        if rs > 85:
            self.score = 5000
            self.count = 3
        if rs > 95:
            self.score = 10000
            self.count = 6
        if rs > 98:
            self.score = 50000
            self.count = 10

    def execute(self):
        while self.status:
            self.count += 4
            rt = random.randint(self.count, self.count * 20)
            time.sleep(rt / 5.0)
            self.playScore()

    def playScore(self):
        betScoreAction = BaiRenBetScoreAction()
        betScore = betScoreAction.betScore.add()
        betScore.score = self.score
        betScore.index = self.index
        sendAction = ReqSendAction()
        sendAction.actionType = 2
        sendAction.data = betScoreAction.SerializeToString()
        self.client.send_data(APPLY_ACTION, sendAction)

    def close(self):
        self.status = False
