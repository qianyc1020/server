import time
import traceback

import core.globalvar as gl


def execute(roomNo, messageHandle):
    time.sleep(12)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            from game.hongbao.mode.hongbao_room import HongbaoRoom
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            from game.hongbao.command.game import gamestart_cmd
            gamestart_cmd.execute(room, messageHandle)
            room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
