# coding=utf-8
import traceback
from Queue import Empty

import core.globalvar as gl
from protocol.base.base_pb2 import NetMessage, LOGIN_SVR
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
                netMessage = NetMessage()
                netMessage.ParseFromString(s.data)
                if s.userId in gl.get_v("clients"):
                    if netMessage.opcode == LOGIN_SVR:
                        gl.get_v("clients")[s.userId].close()
                    else:
                        gl.get_v("serverlogger").logger.info("转发%d消息给%d" % (netMessage.opcode, s.userId))
                        gl.get_v("clients")[s.userId].send(s.data)

            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
