# coding=utf-8
from Queue import Empty

import core.globalvar as gl
from protocol.base.gateway_pb2 import GateWayMessage


class ServerReceive(object):
    __close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                s = GateWayMessage()
                s.ParseFromString(message)

                gl.get_v("clients")[s.userId].send(s.data)
                gl.get_v("serverlogger").logger("转发消息给%d" % s.userId)
            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")
