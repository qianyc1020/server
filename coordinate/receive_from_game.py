# coding=utf-8
import threading
from Queue import Empty

import core.globalvar as gl


class ReceiveHandle(object):
    __close = False
    __lock = threading.Lock()
    __user_queue = {}

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                gl.get_v("serverlogger").logger('''收到游戏服消息%d''' % message.opcode)
                # if message.opcode == message.REGISTER_SERVICE:

            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")

    def remove(self, userid):
        self.__lock.acquire()
        del self.__user_queue[userid]
        self.__lock.release()
