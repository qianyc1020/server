# coding=utf-8
import threading
import traceback
from Queue import Empty
from decimal import Decimal

import core.globalvar as gl
from core import config
from data.database import data_account
from mode.base.game_item import Game
from protocol.base.base_pb2 import *
from protocol.base.game_base_pb2 import RecApplyChangeMatch
from protocol.base.gateway_pb2 import GateWayMessage
from protocol.base.server_to_game_pb2 import *


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
                message = queue.get(True, 20)
                netMessage = NetMessage()
                netMessage.ParseFromString(message)
                gl.get_v("serverlogger").logger.info('''收到游戏服消息%d''' % netMessage.opcode)
                if netMessage.opcode == REGISTER_SERVICE:
                    reqRegisterGame = ReqRegisterGame()
                    reqRegisterGame.ParseFromString(netMessage.data)
                    if reqRegisterGame.password == config.get("coordinate", "game_connect_pwd"):
                        gl.get_v("games").append(Game(reqRegisterGame.alloc_id, reqRegisterGame.name, netMessage.id))
                if netMessage.opcode == CHANGE_SERVICE_STATE:
                    reqServiceState = ReqServiceState()
                    self.changeServerState(netMessage.id, reqServiceState.state)
                if netMessage.opcode == EXIT_GAME:
                    userExit = UserExit()
                    userExit.ParseFromString(netMessage.data)
                    self.update_currency(userExit.playerId)
                    self.send_to_gateway(EXIT_GAME, None, userExit.playerId)
                if netMessage.opcode == APPLY_CHANGE_MATCH:
                    userExit = UserExit()
                    userExit.ParseFromString(netMessage.data)
                    self.update_currency(userExit.playerId)
                    recApplyChangeMatch = RecApplyChangeMatch()
                    recApplyChangeMatch.gameId = userExit.roomNo
                    recApplyChangeMatch.level = userExit.level
                    self.send_to_gateway(APPLY_CHANGE_MATCH, recApplyChangeMatch, userExit.playerId)
            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()

    def changeServerState(self, uuid, state):
        for g in gl.get_v("games"):
            if g.uuid == uuid:
                g.state = state
                self.sendToGame(uuid, CHANGE_SERVICE_STATE, None)
                if g.state == EXITING:
                    gl.get_v("games").remove(g)
                break

    def sendToGame(self, uuid, opcode, data):
        message = NetMessage()
        message.opcode = opcode
        if data is not None:
            message.data = data.SerializeToString()
        gl.get_v("serverlogger").logger.info("发送%d给游戏服" % opcode)
        gl.get_v("redis").publish(uuid, message.SerializeToString())

    def update_currency(self, userId):
        account = data_account.query_account_by_id(None, userId)
        if None is not account:
            currency = RecUpdateCurrency()
            currency.currency = int(account.gold.quantize(Decimal('0')))
            currency.gold = int(account.gold.quantize(Decimal('0')))
            currency.integral = int(account.integral.quantize(Decimal('0')))
            self.send_to_gateway(UPDATE_CURRENCY, currency, userId)

    def send_to_gateway(self, opcode, data, userId):
        send_data = NetMessage()
        send_data.opcode = opcode
        if data is not None:
            send_data.data = data.SerializeToString()

        s = GateWayMessage()
        s.userId = userId
        s.data = send_data.SerializeToString()
        gl.get_v("redis").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, userId))
