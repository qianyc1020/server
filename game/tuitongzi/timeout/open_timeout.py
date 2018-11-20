import time
import traceback

import core.globalvar as gl
from game.tuitongzi.command.game import gameover_cmd
from game.tuitongzi.mode.game_status import GameStatus
from game.tuitongzi.mode.tuitongzi_room import TuitongziRoom


def execute(roomNo, round, messageHandle):
    time.sleep(6)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), TuitongziRoom(), TuitongziRoom().object_to_dict)
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING:
                room.executeAction(0, 5, None, messageHandle)
                room.opencard = True
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
