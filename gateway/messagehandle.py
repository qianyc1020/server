# coding=utf-8
from Queue import Empty

import gateway.globalvar as gl
from protocol.base.gateway_pb2 import GateWayMessage


class MessageHandle(object):
    __close = False
    __userId = None

    def __init__(self, userid):
        self.__userId = userid

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                s = GateWayMessage()
                s.userId = self.__userId
                s.data = message
                gl.get_v("natsobj").publish("server-center", s.SerializeToString())
            except Empty:
                print("messagehandle received timeout")
