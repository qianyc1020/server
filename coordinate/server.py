# coding=utf-8
import Queue
import threading

import coordinate.globalvar as gl
from coordinate.serverreceive import ServerReceive
from utils.logger_utils import LoggerUtils
from utils.natsutils import NatsUtils


def messagehandle(msg):
    gl.get_v("serverqueue").put(msg.data)


class Server(object):

    @staticmethod
    def start():
        gl.init()
        gl.set_v("serverlogger", LoggerUtils("coordinate"))
        gl.set_v("serverqueue", Queue.Queue())
        gl.set_v("natsobj",
                 NatsUtils(["nats://pengyi:pengyi19960207@127.0.0.1:1111"], "server-coordinate", messagehandle))

        t = threading.Thread(target=ServerReceive.handle, args=(ServerReceive(), gl.get_v("serverqueue"),),
                             name='handle')
        t.start()
        gl.get_v("natsobj").startNats()
