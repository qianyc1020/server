# coding=utf-8
import Queue
import threading
from Queue import Empty

import core.globalvar as gl
from game.longhu.usermessagehandle import UserMessageHandle
from protocol.base.base_pb2 import NetMessage
from protocol.base.gateway_pb2 import GateWayMessage


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
                s = GateWayMessage()
                s.ParseFromString(message)
                netMessage = NetMessage()
                netMessage.ParseFromString(s.data)
                gl.get_v("serverlogger").logger('''收到%d消息%d''' % (s.userId, netMessage.opcode))

                self.__lock.acquire()
                if s.userId not in self.__user_queue:
                    messagequeue = Queue.Queue()
                    messagehandle = UserMessageHandle(s.userId, self)
                    t = threading.Thread(target=UserMessageHandle.handle, args=(messagehandle, messagequeue,),
                                         name='handle')  # 线程对象.
                    t.start()
                    self.__user_queue[s.userId] = messagequeue

                self.__user_queue[s.userId].put(netMessage)
                self.__lock.release()
            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")

    def sendToGateway(self, userid, opcode, data):

        netMessage = NetMessage()
        netMessage.opcode = opcode
        if data is not None:
            netMessage.content = data.SerializeToString()

        message = GateWayMessage()
        message.userId = userid
        message.data = netMessage.SerializeToString()

        gl.get_v("serverlogger").logger("发送%d给%d" % (opcode, userid))
        gl.get_v("natsobj").publish("server-gateway", message.SerializeToString())

    def remove(self, userid):
        self.__lock.acquire()
        if userid in self.__user_queue:
            del self.__user_queue[userid]
        self.__lock.release()