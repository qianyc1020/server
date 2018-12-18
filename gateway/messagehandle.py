# coding=utf-8
import traceback
from Queue import Empty

import core.globalvar as gl
from protocol.base.gateway_pb2 import GateWayMessage


class MessageHandle(object):

    def __init__(self, userid):
        self.__userId = userid
        self.__close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                messages = queue.getall(20, True, 20)
                for message in messages:
                    s = GateWayMessage()
                    s.userId = self.__userId
                    s.data = message.SerializeToString()
                    gl.get_v("redis").publish("gateway-coordinate", s.SerializeToString())
            except Empty:
                print("messagehandle received timeout")
            except:
                print traceback.print_exc()
