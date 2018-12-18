# coding=utf-8
import time
import traceback

import core.globalvar as gl


class SendScores(object):

    def __init__(self, roomNo, messageHandle):
        self._close = False
        self.roomNo = roomNo
        self.messageHandle = messageHandle

    def close(self):
        self._close = True

    def execute(self):

        while not self._close:
            time.sleep(0.08)

            redis = gl.get_v("redis")
            if redis.exists("room_" + str(self.roomNo)):
                redis.lock("lockroom_" + str(self.roomNo))
                try:
                    room = redis.getobj("room_" + str(self.roomNo))
                    if 0 != len(room.betScores):
                        room.sendBetScore(self.messageHandle)
                        room.save(redis)
                except:
                    print traceback.print_exc()
                redis.unlock("lockroom_" + str(self.roomNo))
