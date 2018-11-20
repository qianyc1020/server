# coding=utf-8
import time

from data.database import data_record


def execute(room, users, scores):
    t = int(time.time())
    data_record.create_record(str(t) + str(room.roomNo), 7, str(room.roomNo), "", users, scores, t)
