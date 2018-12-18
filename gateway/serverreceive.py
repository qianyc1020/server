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
                message = queue.getall(True, 20)
                gl.get_v("serverlogger").logger.info("2收到消息")
                for m in message:
                    s = GateWayMessage()
                    s.ParseFromString(m)
                    if s.userId in gl.get_v("clients"):
                        gl.get_v("clients")[s.userId].check_and_send(s.data)

            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
