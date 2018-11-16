# coding=utf-8
import time
import traceback

import core.globalvar as gl
from data.database import data_record
from game.longhu.mode.longhu_room import LonghuRoom
from protocol.base.base_pb2 import PLAYER_VOICE
from protocol.base.game_base_pb2 import ReqGpsInfo


def execute(room, users, scores):
    t = int(time.time())
    data_record.create_record(str(t) + str(room.roomNo), 8, str(room.roomNo), "", users, scores, t)
