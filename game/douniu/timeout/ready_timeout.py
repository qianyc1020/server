import time
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus


def execute(round, roomNo, messageHandle, userId, intoDate):
    time.sleep(15)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            from game.douniu.mode.douniu_room import DouniuRoom
            room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
            if room.gameCount == round and room.gameStatus != GameStatus.PLAYING:
                seat = room.getSeatByUserId(userId)
                if seat is not None and not seat.ready and seat.intoDate == intoDate:
                    room.exit(userId, messageHandle)
                    room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
