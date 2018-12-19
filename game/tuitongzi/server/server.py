# coding=utf-8
import json
import threading

import core.globalvar as gl
from core import config
from game.base.game_details_handle import GameDetailsHandle
from game.base.update_currency_handle import UpdateCurrencyHandle
from game.tuitongzi.command.client import match_cmd, reconnection_cmd, exit_cmd, shangzhuang_cmd, xiazhuang_cmd, \
    jixudangzhuang_cmd, watchseat_cmd, change_online
from game.base.game_handle import ReceiveHandle as game_handle
from game.base.rebate_handle import RebateHandle as rebate_handle
from game.tuitongzi.server.command import chat_cmd, interaction_cmd, action_cmd, gps_cmd, voice_cmd, currency_cmd
from protocol.base.base_pb2 import NetMessage, REGISTER_SERVICE
from protocol.base.gateway_pb2 import GateWayMessage
from protocol.base.server_to_game_pb2 import ReqRegisterGame
from utils.TestQueue import TestQueue
from utils.logger_utils import LoggerUtils
from utils.redis_utils import RedisUtils
from utils.stringutils import StringUtils


def message_handle(msg):
    gl.get_v("message-handle-queue").put(msg)


class Server(object):

    @staticmethod
    def start():
        gl.set_v("serverlogger", LoggerUtils("tuitongzi"))
        gl.set_v("message-handle-queue", TestQueue())
        gl.set_v("rebate-handle-queue", TestQueue())
        gl.set_v("update_currency", TestQueue())
        gl.set_v("game_details", TestQueue())
        gl.set_v("play-handle", {})
        uuid = StringUtils.randomStr(32)
        gl.set_v("uuid", uuid)
        gl.set_v("redis", RedisUtils())
        gl.get_v("redis").startSubscribe([uuid], [message_handle])
        gl.set_v("match_info", json.loads(config.get("tuitongzi", "match")))

        threading.Thread(target=game_handle.handle, args=(game_handle(), gl.get_v("message-handle-queue"),),
                         name='message-handle-queue').start()

        threading.Thread(target=rebate_handle.handle,
                         args=(rebate_handle(), gl.get_v("rebate-handle-queue"),),
                         name='rebate-handle-queue').start()

        threading.Thread(target=GameDetailsHandle.handle,
                         args=(GameDetailsHandle(), gl.get_v("game_details"),),
                         name='game_details').start()

        threading.Thread(target=UpdateCurrencyHandle.handle,
                         args=(UpdateCurrencyHandle(), gl.get_v("update_currency"),),
                         name='update_currency').start()

        Server.initCommand()
        Server.register()

    @staticmethod
    def initCommand():
        gl.set_v("command", {})
        gl.get_v("command")["8"] = exit_cmd
        gl.get_v("command")["13"] = reconnection_cmd
        gl.get_v("command")["30"] = action_cmd
        gl.get_v("command")["32"] = chat_cmd
        gl.get_v("command")["33"] = voice_cmd
        gl.get_v("command")["37"] = gps_cmd
        gl.get_v("command")["38"] = interaction_cmd
        gl.get_v("command")["117"] = shangzhuang_cmd
        gl.get_v("command")["118"] = xiazhuang_cmd
        gl.get_v("command")["122"] = jixudangzhuang_cmd
        gl.get_v("command")["124"] = watchseat_cmd
        gl.get_v("command")["1004"] = currency_cmd
        gl.get_v("command")["1005"] = change_online
        gl.get_v("command")["10001"] = match_cmd

    @staticmethod
    def send_to_gateway(self, opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data.SerializeToString()

        s = GateWayMessage()
        s.userId = self.__userId
        s.data = send_data.SerializeToString()
        gl.get_v("redis").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, self.__userId))

    @staticmethod
    def send_to_coordinate(opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data.SerializeToString()
        send_data.id = gl.get_v("uuid")
        gl.get_v("redis").publish("game-coordinate", send_data.SerializeToString())

    @staticmethod
    def register():
        reqRegisterGame = ReqRegisterGame()
        reqRegisterGame.password = config.get("coordinate", "game_connect_pwd")
        reqRegisterGame.alloc_id = 7
        reqRegisterGame.name = "lhd"
        Server.send_to_coordinate(REGISTER_SERVICE, reqRegisterGame)
