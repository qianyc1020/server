# coding=utf-8
import traceback
from Queue import Empty

import core.globalvar as gl
from protocol.base.gateway_pb2 import GateWayMessage


class ServerReceive(object):

    def __init__(self):
        self.__close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                s = GateWayMessage()
                s.ParseFromString(message)

                gl.get_v("clients")[s.userId].send(s.data)
                gl.get_v("serverlogger").logger.info("转发消息给%d" % s.userId)
            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
