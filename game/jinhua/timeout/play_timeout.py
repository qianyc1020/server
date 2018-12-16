import time
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus


def execute(roomNo, messageHandle, userId, gameCount, round):
    time.sleep(60)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameCount == gameCount and room.gameStatus == GameStatus.PLAYING:
                seat = room.getSeatByUserId(userId)
                if not seat.end and seat.round == round:
                    room.abandon(messageHandle, seat)
                    room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
