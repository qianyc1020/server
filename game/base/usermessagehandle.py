# coding=utf-8
import Queue
import threading
import traceback
from Queue import Empty

import core.globalvar as gl
from data.database import data_account, data_gold
from protocol.base.base_pb2 import *
from protocol.base.gateway_pb2 import GateWayMessage


class UserMessageHandle(object):

    def __init__(self, userid, server_receive):
        self.__close = False
        self.__userId = userid
        self.__server_receive = server_receive
        self.sendQueue = Queue.Queue()
        threading.Thread(target=self.relSend, name="clientsend").start()

    def close(self):
        self.__close = True
        self.__server_receive.remove(self.__userId)

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                if str(message.opcode) in gl.get_v("command"):
                    gl.get_v("command")[str(message.opcode)].execute(self.__userId, message, self)
                else:
                    gl.get_v("serverlogger").logger.info("%d消息头不存在%d" % (self.__userId, message.opcode))

            except Empty:
                print("%d messagehandle received timeout close" % self.__userId)
                self.close()
                self.__server_receive.remove(self.__userId)
            except:
                print traceback.print_exc()

    def relSend(self):
        while not self.__close:
            try:
                s = self.sendQueue.get(True, 20)
                gl.get_v("redis").publish("server-gateway", s.SerializeToString())
            except Queue.Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()

    def send_to_gateway(self, opcode, data, userId=None):
        if self.__close:
            return
        send_data = NetMessage()
        send_data.opcode = opcode
        if data is not None:
            send_data.data = data.SerializeToString()
        s = GateWayMessage()
        if userId is None:
            s.userId = self.__userId
        else:
            s.userId = userId
        s.data = send_data.SerializeToString()
        self.sendQueue.put(s)
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, self.__userId if userId is None else userId))

    def game_update_currency(self, gold, id, roomNo):
        data_account.update_currency(None, gold, 0, 0, 0, id)
        data_gold.create_gold(1, roomNo, id, gold)

    def broadcast_seat_to_gateway(self, opcode, data, room):
        for s in room.seats:
            self.send_to_gateway(opcode, data, s.userId)

    def broadcast_watch_to_gateway(self, opcode, data, room):
        for s in room.watchSeats:
            self.send_to_gateway(opcode, data, s.userId)

    def broadcast_all_to_gateway(self, opcode, data, room):
        self.broadcast_seat_to_gateway(opcode, data, room)
        self.broadcast_watch_to_gateway(opcode, data, room)
