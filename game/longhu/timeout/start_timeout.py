import time
import traceback

import core.globalvar as gl
from game.longhu.mode.longhu_room import LonghuRoom


def execute(roomNo, messageHandle):
    time.sleep(11)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)
            from game.longhu.command.game import gamestart_cmd
            gamestart_cmd.execute(room, messageHandle)
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
