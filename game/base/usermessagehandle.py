# coding=utf-8
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

    def close(self):
        self.__close = True
        self.__server_receive.remove(self.__userId)

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                if gl.get_v("command").has_key(str(message.opcode)):
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
        gl.get_v("natsobj").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, self.__userId if userId is None else userId))

    def game_update_currency(self, gold, id, roomNo):
        data_account.update_currency(None, gold, 0, 0, 0, id)
        data_gold.create_gold(1, roomNo, id, gold)

    def broadcast_seat_to_gateway(self, opcode, data, room):
        for s in room.watchSeats:
            self.send_to_gateway(opcode, data, s.userId)

    def broadcast_watch_to_gateway(self, opcode, data, room):
        for s in room.watchSeats:
            self.send_to_gateway(opcode, data, s.userId)

    def broadcast_all_to_gateway(self, opcode, data, room):
        self.broadcast_seat_to_gateway(opcode, data, room)
        self.broadcast_watch_to_gateway(opcode, data, room)