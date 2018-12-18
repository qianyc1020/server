# coding=utf-8
import Queue
import threading
import traceback

import core.globalvar as gl
from game.base.usermessagehandle import UserMessageHandle
from protocol.base.base_pb2 import NetMessage
from protocol.base.gateway_pb2 import GateWayMessage
from utils.TestQueue import TestQueue


class ReceiveHandle(object):

    def __init__(self):
        self.__close = False
        self.__lock = threading.Lock()
        self.__user_queue = {}
        self.sendQueue = TestQueue()
        threading.Thread(target=self.relSend, name="clientsend").start()

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                messages = queue.getall(30, True, 20)
                for message in messages:
                    s = GateWayMessage()
                    s.ParseFromString(message)
                    netMessage = NetMessage()
                    netMessage.ParseFromString(s.data)
                    gl.get_v("serverlogger").logger.info('''收到%d消息%d''' % (s.userId, netMessage.opcode))

                    self.__lock.acquire()
                    if s.userId not in self.__user_queue:
                        messagequeue = TestQueue()
                        messagehandle = UserMessageHandle(s.userId, self)
                        threading.Thread(target=UserMessageHandle.handle, args=(messagehandle, messagequeue,),
                                         name='handle').start()  # 线程对象.
                        self.__user_queue[s.userId] = messagequeue

                    self.__user_queue[s.userId].put(netMessage)
                    self.__lock.release()
            except Queue.Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()

    def relSend(self):
        while not self.__close:
            try:
                ss = self.sendQueue.getall(20, True, 20)
                for s in ss:
                    gl.get_v("redis").publish("server-gateway", s)
            except Queue.Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()

    def remove(self, userid):
        self.__lock.acquire()
        if userid in self.__user_queue:
            del self.__user_queue[userid]
        self.__lock.release()
