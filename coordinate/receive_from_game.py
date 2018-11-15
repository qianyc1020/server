# coding=utf-8
import threading
import traceback
from Queue import Empty

import core.globalvar as gl
from core import config
from mode.base.game_item import Game
from protocol.base.base_pb2 import *
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
                gl.get_v("serverlogger").logger('''收到游戏服消息%d''' % netMessage.opcode)
                if netMessage.opcode == REGISTER_SERVICE:
                    reqRegisterGame = ReqRegisterGame()
                    reqRegisterGame.ParseFromString(netMessage.data)
                    if reqRegisterGame.password == config.get("coordinate", "game_connect_pwd"):
                        gl.get_v("games").append(Game(reqRegisterGame.alloc_id, reqRegisterGame.name, netMessage.id))
                if netMessage.opcode == CHANGE_SERVICE_STATE:
                    reqServiceState = ReqServiceState()
                    self.changeServerState(netMessage.id, reqServiceState.state)

            except Empty:
                gl.get_v("serverlogger").logger("Received timeout")
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
        gl.get_v("serverlogger").logger("发送%d给游戏服" % opcode)
        gl.get_v("natsobj").publish(uuid, message.SerializeToString())
