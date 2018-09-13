# coding=utf-8
from Queue import Empty

import coordinate.globalvar as gl
from protocol.base.base_pb2 import NetMessage
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

                netmessage = NetMessage()
                netmessage.ParseFromString(s.data)
                gl.get_v("serverlogger").logger('''收到%d消息%d''' % (s.userId, netmessage.opcode))

            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")
