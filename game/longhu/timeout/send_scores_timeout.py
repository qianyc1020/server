# coding=utf-8
import time
import traceback

import core.globalvar as gl
from protocol.base.base_pb2 import EXECUTE_ACTION


class SendScores(object):

    def __init__(self, roomNo, messageHandle):
        self._close = False
        self.roomNo = roomNo
        self.messageHandle = messageHandle

    def close(self):
        self._close = True

    def execute(self):

        while not self._close:
            time.sleep(0.05)

            redis = gl.get_v("redis")
            if redis.exists("room_" + str(self.roomNo)):
                gl.get_v("serverlogger").logger.info("下注加锁前")
                redis.lock("lockroom_" + str(self.roomNo))
                try:
                    room = redis.getobj("room_" + str(self.roomNo))
                    if 0 != len(room.betScores):
                        senddata = room.getSendBetScore()
                        room.save(redis)
                        redis.unlock("lockroom_" + str(self.roomNo))
                        gl.get_v("serverlogger").logger.info("下注发送前")
                        self.messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, senddata, self)
                        gl.get_v("serverlogger").logger.info("下注发送完成")

                except:
                    print traceback.print_exc()
                    redis.unlock("lockroom_" + str(self.roomNo))
