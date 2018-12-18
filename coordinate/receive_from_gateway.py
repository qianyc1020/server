# coding=utf-8
import threading
import traceback
from Queue import Empty

import core.globalvar as gl
from coordinate.usermessagehandle import UserMessageHandle
from protocol.base.base_pb2 import NetMessage
from protocol.base.gateway_pb2 import GateWayMessage
from utils.TestQueue import TestQueue


class ReceiveHandle(object):

    def __init__(self):
        self.__close = False
        self.__lock = threading.Lock()
        self.__user_queue = {}

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                messages = queue.getall(20, True, 20)
                for message in messages:
                    s = GateWayMessage()
                    s.ParseFromString(message)

                    netmessage = NetMessage()
                    netmessage.ParseFromString(s.data)
                    gl.get_v("serverlogger").logger.info('''收到%d消息%d''' % (s.userId, netmessage.opcode))

                    self.__lock.acquire()
                    if s.userId not in self.__user_queue:
                        messagequeue = TestQueue()
                        messagehandle = UserMessageHandle(s.userId, self)
                        t = threading.Thread(target=messagehandle.handle, args=(messagequeue,),
                                             name='handle')  # 线程对象.
                        t.start()
                        self.__user_queue[s.userId] = messagequeue

                    self.__user_queue[s.userId].put(netmessage)
                    self.__lock.release()
            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()

    def remove(self, userid):
        self.__lock.acquire()
        if userid in self.__user_queue:
            del self.__user_queue[userid]
        self.__lock.release()
