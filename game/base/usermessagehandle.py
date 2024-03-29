# coding=utf-8
import traceback
from Queue import Empty

import core.globalvar as gl
from protocol.base.base_pb2 import *
from protocol.base.gateway_pb2 import GateWayMessage


class UserMessageHandle(object):

    def __init__(self, userid, server_receive):
        self.__close = False
        self.__userId = userid
        self.__server_receive = server_receive
        self.send_data = NetMessage()
        self.s = GateWayMessage()

    def close(self):
        self.__close = True
        self.__server_receive.remove(self.__userId)

    def handle(self, queue):
        while not self.__close:
            try:
                messages = queue.getall(20, True, 20)
                for message in messages:
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

    def send_to_gateway(self, opcode, data, userId=None):
        self.send_data.Clear()
        self.send_data.opcode = opcode
        if data is not None:
            self.send_data.data = data.SerializeToString()
        if userId is None:
            self.s.userId = self.__userId
        else:
            self.s.userId = userId
        self.s.data = self.send_data.SerializeToString()
        self.__server_receive.sendQueue.put(self.s.SerializeToString())
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, self.__userId if userId is None else userId))

    def get_send_data(self, opcode, data):
        self.send_data.Clear()
        self.send_data.opcode = opcode
        if data is not None:
            self.send_data.data = data.SerializeToString()

    def broadcast_seat_to_gateway(self, opcode, data, room):
        for s in room.seats:
            self.send_to_gateway(opcode, data, s.userId)

    def broadcast_watch_to_gateway(self, opcode, data, room):
        gl.get_v("serverlogger").logger.info("发送之前")
        self.get_send_data(opcode, data)
        datas = []
        for s in room.watchSeats:
            if s.userId is None:
                self.s.userId = self.__userId
            else:
                self.s.userId = s.userId
            self.s.data = self.send_data.SerializeToString()
            datas.append(self.s.SerializeToString())
        self.__server_receive.sendQueue.putall(datas)
        gl.get_v("serverlogger").logger.info("发送之后")

    def broadcast_all_to_gateway(self, opcode, data, room):
        self.broadcast_seat_to_gateway(opcode, data, room)
        self.broadcast_watch_to_gateway(opcode, data, room)
