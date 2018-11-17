# coding=utf-8
import time

from data.database import data_record


def execute(room, users, scores):
    t = int(time.time())
    for i in range(0, 100000):
        data_record.create_record(str(t + i) + str(room.roomNo), 8, str(room.roomNo), "", users, scores, t)
