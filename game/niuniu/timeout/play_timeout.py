import time
import traceback

import core.globalvar as gl
from game.niuniu.command.game import gameover_cmd
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.mode.niuniu_room import NiuniuRoom


def execute(roomNo, messageHandle, round):
    time.sleep(20)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), NiuniuRoom(), NiuniuRoom().object_to_dict)
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING:
                gameover_cmd.execute(room, messageHandle)
                redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
