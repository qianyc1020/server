# coding=utf-8
import threading
from Queue import Empty

import core.globalvar as gl
from protocol.base.gateway_pb2 import GateWayMessage
from protocol.base.server_to_game_pb2 import *


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
                gl.get_v("serverlogger").logger('''收到消息%d''' % message.opcode)

            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")

    def sendToGateway(self, userid, opcode, data):

        netMessage = NetMessage()
        netMessage.msgHead = opcode
        if data is not None:
            netMessage.content = data.SerializeToString()

        message = GateWayMessage()
        message.userId = userid
        message.data = netMessage.SerializeToString()

        gl.get_v("natsobj").publish("server-gateway", message.SerializeToString())
