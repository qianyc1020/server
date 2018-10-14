# coding=utf-8
class Position(object):
    cards = []
    playScores = {}
    totalScore = 0

    def clear(self):
        self.cards = []
        self.playScores = {}
        self.totalScore = 0
