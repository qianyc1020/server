# coding=utf-8
from Queue import Empty
from decimal import Decimal

import core.globalvar as gl
from data.database import data_account
from protocol.base.base_pb2 import *
from protocol.base.gateway_pb2 import GateWayMessage
from protocol.base.server_to_game_pb2 import RUNNING
from protocol.service.match_pb2 import *


class UserMessageHandle(object):
    __close = False
    __userId = None
    __server_receive = None
    __redis = None

    def __init__(self, userid, server_receive):
        self.__userId = userid
        self.__server_receive = server_receive
        self.__redis = gl.get_v("redis")

    def close(self):
        self.__close = True
        self.__server_receive.remove(self.__userId)

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                if message.opcode == APPLY_ENTER_MATCH:
                    reqApplyEnterMatch = ReqApplyEnterMatch()
                    reqApplyEnterMatch.ParseFromString(message.data)
                    find = False
                    for g in gl.get_v("games"):
                        if g.alloc_id == reqApplyEnterMatch.allocId and g.state == RUNNING:
                            self.sendToGame(g.uuid, APPLY_ENTER_MATCH, reqApplyEnterMatch.SerializeToString())
                            find = True
                            recApplyEnterMatch = RecApplyEnterMatch()
                            recApplyEnterMatch.state = recApplyEnterMatch.SUCCESS
                            self.send_to_gateway(APPLY_ENTER_MATCH, recApplyEnterMatch)
                            break
                    if not find:
                        recApplyEnterMatch = RecApplyEnterMatch()
                        recApplyEnterMatch.state = recApplyEnterMatch.FAILD
                        self.send_to_gateway(APPLY_ENTER_MATCH, recApplyEnterMatch)

                elif message.opcode == UPDATE_MATCH_INFO:
                    reqUpdateMatchInfo = ReqUpdateMatchInfo()
                    reqUpdateMatchInfo.ParseFromString(message.data)

                    recUpdateMatchInfo = RecUpdateMatchInfo()
                    recUpdateMatchInfo.allocId = reqUpdateMatchInfo.allocId
                    recUpdateMatchInfo.level = reqUpdateMatchInfo.level
                    recUpdateMatchInfo.games = 1
                    recUpdateMatchInfo.players = 5
                    recUpdateMatchInfo.totalPlayers = 10
                    self.send_to_gateway(UPDATE_MATCH_INFO, recUpdateMatchInfo)

                elif message.opcode == BANK_INFO:
                    reqBankInfo = ReqBankInfo()
                    reqBankInfo.ParseFromString(message.data)

                    account = data_account.query_account_by_id(None, self.__userId)

                    recBankInfo = RecBankInfo()
                    recBankInfo.card = int(account.bank_gold.quantize(Decimal('0')))
                    recBankInfo.gold = int(account.bank_gold.quantize(Decimal('0')))
                    recBankInfo.integral = int(account.bank_integral.quantize(Decimal('0')))
                    self.send_to_gateway(BANK_INFO, recBankInfo)

                elif message.opcode == BANK_DEPOSIT or message.opcode == BANK_GET:
                    reqOperateBank = ReqOperateBank()
                    reqOperateBank.ParseFromString(message.data)
                    account = data_account.query_account_by_id(None, self.__userId)
                    if message.opcode == BANK_DEPOSIT and int(
                            account.gold.quantize(Decimal('0'))) < reqOperateBank.card:
                        break
                    if message.opcode == BANK_DEPOSIT and int(
                            account.gold.quantize(Decimal('0'))) < reqOperateBank.gold:
                        break
                    if message.opcode == BANK_DEPOSIT and int(
                            account.integral.quantize(Decimal('0'))) < reqOperateBank.integral:
                        break
                    if message.opcode == BANK_GET and int(
                            account.bank_gold.quantize(Decimal('0'))) < reqOperateBank.card:
                        break
                    if message.opcode == BANK_GET and int(
                            account.bank_gold.quantize(Decimal('0'))) < reqOperateBank.gold:
                        break
                    if message.opcode == BANK_GET and int(
                            account.bank_integral.quantize(Decimal('0'))) < reqOperateBank.integral:
                        break
                    gold = reqOperateBank.card if message.opcode == BANK_DEPOSIT else -reqOperateBank.card
                    integral = reqOperateBank.integral if message.opcode == BANK_DEPOSIT else -reqOperateBank.integral

                    data_account.update_currency(None, gold, integral, -gold, -integral, self.__userId)

                    recOprateBank = RecOprateBank()
                    self.send_to_gateway(message.opcode, recOprateBank)

                    account = data_account.query_account_by_id(None, self.__userId)
                    self.update_currency(account)
                elif message.opcode == UPDATE_RANK:
                    reqGameRank = ReqGameRank()
                    reqGameRank.ParseFromString(message.data)
                    accounts = data_account.ranking_by_gold(None, reqGameRank.number)
                    recGameRank = RecGameRank()
                    i = 0
                    for a in accounts:
                        i += 1
                        playerRankInfo = recGameRank.playerDatas.add()
                        playerRankInfo.rankId = i
                        playerRankInfo.playerId = a.id
                        playerRankInfo.currency = int(a.gold.quantize(Decimal('0')))
                        playerRankInfo.nick = a.nick_name
                        playerRankInfo.headUrl = a.head_url
                        if a.introduce is not None:
                            playerRankInfo.introduce = a.introduce
                        playerRankInfo.consumeVip = a.level
                    self.send_to_gateway(message.opcode, recGameRank)
                elif (5 < message.opcode < 23) or (27 < message.opcode < 34) or (
                        99 < message.opcode < 200) or message.opcode == 38:
                    roomNo = self.__redis.get(str(self.__userId) + "_room")
                    gameId = self.__redis.get(str(roomNo) + "_gameId")
                    for g in gl.get_v("games"):
                        if g.alloc_id == gameId and g.state == RUNNING:
                            self.sendToGame(g.uuid, message.opcode, message.data)
                            break

            except Empty:
                print("%d messagehandle received timeout close" % self.__userId)
                self.close()
                self.__server_receive.remove(self.__userId)

    def send_to_gateway(self, opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data.SerializeToString()

        s = GateWayMessage()
        s.userId = self.__userId
        s.data = send_data.SerializeToString()
        gl.get_v("natsobj").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger("发送%d给%s" % (opcode, self.__userId))

    def sendToGame(self, uuid, opcode, data):
        message = NetMessage()
        message.opcode = opcode
        if data is not None:
            message.data = data
        s = GateWayMessage()
        s.userId = self.__userId
        s.data = message.SerializeToString()
        gl.get_v("serverlogger").logger("%d发送%d给游戏服" % (self.__userId, opcode))
        gl.get_v("natsobj").publish(uuid.encode("utf-8"), s.SerializeToString())

    def update_currency(self, account):
        currency = RecUpdateCurrency()
        currency.currency = int(account.gold.quantize(Decimal('0')))
        currency.gold = int(account.gold.quantize(Decimal('0')))
        currency.integral = int(account.integral.quantize(Decimal('0')))
        self.send_to_gateway(UPDATE_CURRENCY, currency)
