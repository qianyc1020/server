# coding=utf-8
from decimal import Decimal

from mode.game.seat import Seat


class LonghuSeat(Seat):
    playScore = Decimal(0)
    intoDate = None
    shangzhuangScore = Decimal(0)

    def clear(self):
        self.playScore = 0
