import time
import traceback

import core.globalvar as gl
from game.tuitongzi.command.game import gameover_cmd
from game.tuitongzi.mode.game_status import GameStatus


def execute(roomNo, messageHandle, round):
    time.sleep(20)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING:
                gameover_cmd.execute(room, messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
