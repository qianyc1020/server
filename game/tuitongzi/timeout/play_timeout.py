import time
import traceback

import core.globalvar as gl
from game.tuitongzi.command.game import gameover_cmd
from game.tuitongzi.mode.tuitongzi_room import TuitongziRoom


def execute(roomNo, messageHandle):
    time.sleep(20)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), TuitongziRoom(), TuitongziRoom().object_to_dict)
            gameover_cmd.execute(room, messageHandle)
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
