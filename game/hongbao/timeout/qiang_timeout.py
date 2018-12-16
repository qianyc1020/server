import time
import traceback

import core.globalvar as gl
from game.hongbao.command.game import gameover_cmd
from game.hongbao.mode.game_status import GameStatus


def execute(roomNo, round, messageHandle):
    time.sleep(9)

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
