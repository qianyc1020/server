# coding=utf-8
import traceback
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from game.douniu.mode.douniu_room import DouniuRoom


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        account = data_account.query_account_by_id(None, userId)
        if account is not None:
            redis.lock("lockroom_" + str(roomNo), 5000)
            try:
                room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
                seat = room.getSeatByUserId(userId)
                if seat is not None:
                    seat.score = int(account.gold.quantize(Decimal('0')))
                room.sendBetScore(messageHandle)
                room.save(redis)
                room.recUpdateScore(messageHandle, 0)

            except:
                print traceback.print_exc()
            redis.unlock("lockroom_" + str(roomNo))
