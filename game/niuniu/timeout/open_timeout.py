import time
import traceback

import core.globalvar as gl
from game.niuniu.mode.game_status import GameStatus


def execute(roomNo, round, messageHandle):
    time.sleep(6)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING:
                room.executeAction(0, 5, None, messageHandle)
                room.opencard = True
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
