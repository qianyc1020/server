import random
import time
import traceback

import core.globalvar as gl
from game.hongbao.mode.game_status import GameStatus


def execute(roomNo, round, messageHandle):
    time.sleep(4)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING and not room.started:
                room.bankerSelectNum(random.randint(0, 9), messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
