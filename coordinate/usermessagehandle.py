# coding=utf-8
from Queue import Empty

from protocol.base.game_base_pb2 import RecMatchGame


class UserMessageHandle(object):
    __close = False
    __userId = None
    __server_receive = None

    def __init__(self, userid, server_receive):
        self.__userId = userid
        self.__server_receive = server_receive

    def close(self):
        self.__close = True
        self.__server_receive.remove(self.__userId)

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                if message.opcode == message.APPLY_ENTER_MATCH:
                    match = RecMatchGame()
                    match.ParseFromString(message.data)
            except Empty:
                print("%d messagehandle received timeout close" % self.__userId)
                self.close()
