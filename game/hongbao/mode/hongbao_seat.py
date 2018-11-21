# coding=utf-8

from mode.game.seat import Seat


class HongbaoSeat(Seat):

    def __init__(self):
        self.playScore = 0
        self.intoDate = None
        self.shangzhuangScore = 0

    def clear(self):
        self.playScore = 0
