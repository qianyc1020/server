import time
import traceback

import core.globalvar as gl
from game.niuniu.command.game import gameover_cmd
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.mode.niuniu_room import NiuniuRoom


def execute(roomNo, round, messageHandle):
    time.sleep(6)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), NiuniuRoom(), NiuniuRoom().object_to_dict)
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING:
                room.executeAction(0, 5, None, messageHandle)
                room.opencard = True
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
