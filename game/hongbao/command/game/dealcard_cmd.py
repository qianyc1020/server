# coding=utf-8
import threading
import time
import traceback

import core.globalvar as gl
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.timeout import selnum_timeout


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.WAITING:
            room.startDate = int(time.time())
            room.executeAsk(messageHandle, room.banker, 1)
            room.gameStatus = GameStatus.PLAYING

            t = threading.Thread(target=selnum_timeout.execute, args=(room.roomNo, room.gameCount, messageHandle,),
                                 name='selnum_timeout')  # 线程对象.
            t.start()
            gl.get_v("serverlogger").logger.info("开始下注")
    except:
        print traceback.print_exc()
