# coding=utf-8

from mode.game.seat import Seat


class LonghuSeat(Seat):

    def __init__(self):
        super(LonghuSeat, self).__init__()
        self.playScore = 0
        self.intoDate = None
        self.shangzhuangScore = 0
        self.lianzhuang = 0

    def clear(self):
        self.playScore = 0
