# coding=utf-8
from Queue import Empty
from decimal import Decimal

import core.globalvar as gl
from data.database import login, mysql_connection
from protocol.base.base_pb2 import *
from protocol.base.game_base_pb2 import RecMatchGame
from protocol.base.gateway_pb2 import GateWayMessage


class UserMessageHandle(object):
    __close = False
    __userId = None
    __server_receive = None

    def __init__(self, userid, server_receive):
        self.__userId = userid
        self.__server_receive = server_receive

    def close(self):
        self.__close = True
        self.__server_receive.remove(self.__userId)

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                if message.opcode == message.APPLY_ENTER_MATCH:
                    match = RecMatchGame()
                    match.ParseFromString(message.data)
                if message.opcode == message.BANK_INFO:
                    reqBankInfo = ReqBankInfo()
                    reqBankInfo.ParseFromString(message.data)

                    account = login.query_account_by_id(mysql_connection.get_conn(), self.__userId)

                    recBankInfo = RecBankInfo()
                    recBankInfo.card = int(account.gold.quantize(Decimal('0')))
                    recBankInfo.gold = int(account.gold.quantize(Decimal('0')))
                    recBankInfo.integral = int(account.integral.quantize(Decimal('0')))
                    self.send_to_gateway(recBankInfo)

            except Empty:
                print("%d messagehandle received timeout close" % self.__userId)
                self.close()

    def send_to_gateway(self, data):
        s = GateWayMessage()
        s.userId = self.__userId
        s.data = data.SerializeToString()
        gl.get_v("natsobj").publish("server-gateway", s.SerializeToString())
