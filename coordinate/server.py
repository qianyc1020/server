# coding=utf-8
import threading

import core.globalvar as gl
from coordinate.receive_from_game import ReceiveHandle as game_handle
from coordinate.receive_from_gateway import ReceiveHandle as gateway_handle
from notice import server
from utils.TestQueue import TestQueue
from utils.logger_utils import LoggerUtils
from utils.redis_utils import RedisUtils


def from_gateway_handle(msg):
    gl.get_v("from-gateway-queue").put(msg)


def from_game_handle(msg):
    gl.get_v("from-game-queue").put(msg)


class Server(object):

    @staticmethod
    def start():
        gl.set_v("serverlogger", LoggerUtils("coordinate"))
        gl.set_v("from-gateway-queue", TestQueue())
        gl.set_v("from-game-queue", TestQueue())
        gl.set_v("games", [])
        gl.set_v("redis", RedisUtils())
        gl.get_v("redis").startSubscribe(["gateway-coordinate", "game-coordinate"],
                                         [from_gateway_handle, from_game_handle])

        threading.Thread(target=gateway_handle.handle, args=(gateway_handle(), gl.get_v("from-gateway-queue"),),
                         name='from-gateway-queue').start()
        threading.Thread(target=game_handle.handle, args=(game_handle(), gl.get_v("from-game-queue"),),
                         name='from-game-queue').start()
        server.start_server()
