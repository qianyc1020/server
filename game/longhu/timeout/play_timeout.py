import time
import traceback

import core.globalvar as gl
from game.longhu.command.game import gameover_cmd
from game.longhu.mode.game_status import GameStatus
from game.longhu.mode.longhu_room import LonghuRoom


def execute(roomNo, messageHandle, round):
    time.sleep(12)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), LonghuRoom(), LonghuRoom().object_to_dict)
            if room.gameCount == round and room.gameStatus == GameStatus.PLAYING:
                gameover_cmd.execute(room, messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
