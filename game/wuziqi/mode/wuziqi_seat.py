# coding=utf-8

from mode.game.seat import Seat


class WuziqiSeat(Seat):

    def __init__(self):
        super(WuziqiSeat, self).__init__()
        self.intoDate = None

    def clear(self):
        pass
