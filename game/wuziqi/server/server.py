# coding=utf-8
import Queue
import threading
import time

import core.globalvar as gl
from core import config
from game.wuziqi.command.client import reconnection_cmd, exit_cmd, create_room_cmd, join_room_cmd, set_amount_cmd, \
    ready_cmd, lose_cmd
from game.base.game_handle import ReceiveHandle as game_handle
from game.wuziqi.server.command import chat_cmd, interaction_cmd, action_cmd, gps_cmd, voice_cmd
from protocol.base.base_pb2 import NetMessage, REGISTER_SERVICE
from protocol.base.gateway_pb2 import GateWayMessage
from protocol.base.server_to_game_pb2 import ReqRegisterGame
from utils.logger_utils import LoggerUtils
from utils.natsutils import NatsUtils
from utils.redis_utils import RedisUtils
from utils.stringutils import StringUtils


def message_handle(msg):
    gl.get_v("message-handle-queue").put(msg.data)


class Server(object):

    @staticmethod
    def start():
        gl.set_v("serverlogger", LoggerUtils("game"))
        gl.set_v("message-handle-queue", Queue.Queue())
        uuid = StringUtils.randomStr(32)
        gl.set_v("uuid", uuid)
        gl.set_v("natsobj", NatsUtils([config.get("nats", "nats")], [uuid], [message_handle]))
        gl.set_v("redis", RedisUtils())

        t = threading.Thread(target=game_handle.handle, args=(game_handle(), gl.get_v("message-handle-queue"),),
                             name='message-handle-queue')
        t.start()

        Server.initCommand()
        natsthread = threading.Thread(target=NatsUtils.startNats, args=(gl.get_v("natsobj"),), name='natsthread')
        natsthread.start()

        while not gl.get_v("natsobj").isConnect():
            time.sleep(2)
        Server.register()

    @staticmethod
    def initCommand():
        gl.set_v("command", {})
        gl.get_v("command")["6"] = create_room_cmd
        gl.get_v("command")["7"] = join_room_cmd
        gl.get_v("command")["8"] = exit_cmd
        gl.get_v("command")["10"] = ready_cmd
        gl.get_v("command")["30"] = action_cmd
        gl.get_v("command")["32"] = chat_cmd
        gl.get_v("command")["33"] = voice_cmd
        gl.get_v("command")["37"] = gps_cmd
        gl.get_v("command")["38"] = interaction_cmd
        gl.get_v("command")["13"] = reconnection_cmd
        gl.get_v("command")["104"] = set_amount_cmd
        gl.get_v("command")["105"] = lose_cmd

    @staticmethod
    def send_to_gateway(self, opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data.SerializeToString()

        s = GateWayMessage()
        s.userId = self.__userId
        s.data = send_data.SerializeToString()
        gl.get_v("natsobj").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, self.__userId))

    @staticmethod
    def send_to_coordinate(opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data.SerializeToString()
        send_data.id = gl.get_v("uuid")
        gl.get_v("natsobj").publish("game-coordinate", send_data.SerializeToString())

    @staticmethod
    def register():
        reqRegisterGame = ReqRegisterGame()
        reqRegisterGame.password = config.get("coordinate", "game_connect_pwd")
        reqRegisterGame.alloc_id = 3
        reqRegisterGame.name = "lhd"
        Server.send_to_coordinate(REGISTER_SERVICE, reqRegisterGame)