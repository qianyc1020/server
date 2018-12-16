import time
import traceback

import core.globalvar as gl


def execute(roomNo, messageHandle):
    time.sleep(12)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            from game.hongbao.command.game import gamestart_cmd
            gamestart_cmd.execute(room, messageHandle)
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
