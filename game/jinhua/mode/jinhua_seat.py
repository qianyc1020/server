# coding=utf-8

from mode.game.seat import Seat


class JinhuaSeat(Seat):

    def __init__(self):
        super(JinhuaSeat, self).__init__()
        self.playScore = 0
        self.intoDate = None
        self.initialCards = []
        self.lookCard = False
        self.end = False
        self.round = 0
        self.guanzhan = False
        self.canLookUser = []
        self.cardType = 0

    def clear(self):
        self.playScore = 0
        self.initialCards = []
        self.lookCard = False
        self.end = False
        self.round = 0
        self.guanzhan = False
        self.canLookUser = []
        self.cardType = 0
