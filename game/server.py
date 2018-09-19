# coding=utf-8
import Queue
import threading

import core.globalvar as gl
from game.game_handle import ReceiveHandle as game_handle
from core import config
from protocol.base.base_pb2 import NetMessage
from utils.logger_utils import LoggerUtils
from utils.natsutils import NatsUtils
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
        gl.set_v("natsobj", NatsUtils([config.get("nats", "nats")], ["uuid"], [message_handle]))

        t = threading.Thread(target=game_handle.handle, args=(game_handle(), gl.get_v("message-handle-queue"),),
                             name='message-handle-queue')
        t.start()

        Server.initCommand()

        gl.get_v("natsobj").startNats()

    @staticmethod
    def initCommand():
        gl.set_v("command", {})
        gl.get_v("command")[NetMessage.] =
