# coding=utf-8
class Position(object):

    def __init__(self):
        self.cards = []
        self.playScores = {}
        self.totalScore = 0

    def clear(self):
        self.cards = []
        self.playScores = {}
        self.totalScore = 0
