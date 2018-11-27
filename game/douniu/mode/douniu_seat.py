# coding=utf-8

from mode.game.seat import Seat


class DouniuSeat(Seat):

    def __init__(self):
        super(DouniuSeat, self).__init__()
        self.playScore = -1
        self.intoDate = None
        self.initialCards = []
        self.openCard = False
        self.grab = -1
        self.tuizhu = 0
        self.guanzhan = False
        self.cardType = 0

    def clear(self):
        self.playScore = -1
        self.initialCards = []
        self.openCard = False
        self.grab = -1
        self.guanzhan = False
        self.cardType = 0
