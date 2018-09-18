# coding=utf-8
import threading
from Queue import Empty

import core.globalvar as gl
from core import config
from mode.game_item import Game
from protocol.base.server_to_game_pb2 import *


class ReceiveHandle(object):
    __close = False
    __lock = threading.Lock()
    __user_queue = {}

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                message = queue.get(True, 20)
                gl.get_v("serverlogger").logger('''收到游戏服消息%d''' % message.opcode)
                if message.opcode == REGISTER_SERVICE:
                    reqRegisterGame = ReqRegisterGame()
                    if reqRegisterGame.password == config.get("coordinate", "game_connect_pwd"):
                        gl.get_v("games").append(Game(reqRegisterGame.alloc_id, reqRegisterGame.name, message.id))
                if message.opcode == CHANGE_SERVICE_STATE:
                    reqServiceState = ReqServiceState()
                    self.changeServerState(message.id, reqServiceState.state)

            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")

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
        message.msgHead = opcode
        if data is not None:
            message.content = data.SerializeToString()
        gl.get_v("natsobj").publish(uuid, message.SerializeToString())
