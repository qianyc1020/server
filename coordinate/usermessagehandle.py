# coding=utf-8
from Queue import Empty
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account, mysql_connection
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

                    account = data_account.query_account_by_id(mysql_connection.get_conn(), self.__userId)

                    recBankInfo = RecBankInfo()
                    recBankInfo.card = int(account.bank_gold.quantize(Decimal('0')))
                    recBankInfo.gold = int(account.bank_gold.quantize(Decimal('0')))
                    recBankInfo.integral = int(account.bank_integral.quantize(Decimal('0')))
                    self.send_to_gateway(NetMessage.BANK_INFO, recBankInfo)

                if message.opcode == message.BANK_DEPOSIT or message.opcode == message.BANK_GET:
                    reqOperateBank = ReqOperateBank()
                    reqOperateBank.ParseFromString(message.data)
                    account = data_account.query_account_by_id(mysql_connection.get_conn(), self.__userId)
                    if message.opcode == message.BANK_DEPOSIT and int(
                            account.gold.quantize(Decimal('0'))) < reqOperateBank.card:
                        break
                    if message.opcode == message.BANK_DEPOSIT and int(
                            account.gold.quantize(Decimal('0'))) < reqOperateBank.gold:
                        break
                    if message.opcode == message.BANK_DEPOSIT and int(
                            account.integral.quantize(Decimal('0'))) < reqOperateBank.integral:
                        break
                    if message.opcode == message.BANK_GET and int(
                            account.bank_gold.quantize(Decimal('0'))) < reqOperateBank.card:
                        break
                    if message.opcode == message.BANK_GET and int(
                            account.bank_gold.quantize(Decimal('0'))) < reqOperateBank.gold:
                        break
                    if message.opcode == message.BANK_GET and int(
                            account.bank_integral.quantize(Decimal('0'))) < reqOperateBank.integral:
                        break
                    gold = reqOperateBank.gold if message.opcode == message.BANK_DEPOSIT else -reqOperateBank.gold
                    integral = reqOperateBank.integral if message.opcode == message.BANK_DEPOSIT else -reqOperateBank.integral

                    data_account.update_currency(mysql_connection.get_conn(), gold, integral, self.__userId)

                    recOprateBank = RecOprateBank()
                    self.send_to_gateway(message.opcode, recOprateBank)

                    account = data_account.query_account_by_id(mysql_connection.get_conn(), self.__userId)
                    self.update_currency(account)


            except Empty:
                print("%d messagehandle received timeout close" % self.__userId)
                self.close()
                self.__server_receive.close()

    def send_to_gateway(self, opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data.SerializeToString()

        s = GateWayMessage()
        s.userId = self.__userId
        s.data = send_data.SerializeToString()
        gl.get_v("natsobj").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger("发送%d给%s" % (opcode, self.__userId))

    def update_currency(self, account):
        currency = RecUpdateCurrency()
        currency.currency = int(account.gold.quantize(Decimal('0')))
        currency.gold = int(account.gold.quantize(Decimal('0')))
        currency.integral = int(account.integral.quantize(Decimal('0')))
        self.send_to_gateway(NetMessage.UPDATE_CURRENCY, currency)
