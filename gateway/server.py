# coding=utf-8
import os
import socket
import threading
import traceback

import core.globalvar as gl
import gateway
import gateway.clientreceive
from core import config
from protocol.base.gateway_pb2 import GateWayMessage
from utils.logger_utils import LoggerUtils
from utils.redis_utils import RedisUtils


def messagehandle(msg):
    s = GateWayMessage()
    s.ParseFromString(msg)
    if -1 == s.userId:
        for client in gl.get_v("clients"):
            client.send(s.data)
    elif s.userId in gl.get_v("clients"):
        gl.get_v("clients")[s.userId].check_and_send(s.data)


class Server(object):

    @staticmethod
    def start():
        try:
            gl.set_v("serverlogger", LoggerUtils("gateway"))
            gl.set_v("redis", RedisUtils())
            gl.get_v("redis").startSubscribe(["server-gateway"], [messagehandle])
            gl.set_v("clients", {})

            ip_port = ('', int(config.get("gateway", "port")))
            sk = socket.socket()
            sk.bind(ip_port)
            sk.listen(5)
            gl.get_v("serverlogger").logger.info("server started")
            while True:
                reload(gateway.clientreceive)
                from gateway.clientreceive import ClientReceive
                conn, address = sk.accept()
                threading.Thread(target=ClientReceive.receive,
                                 args=(ClientReceive(), conn, '''%s:%d''' % (address[0], address[1]),),
                                 name='clientreceive').start()  # 线程对象.
        except:
            print traceback.print_exc()
            for (c, v) in gl.get_v("clients").items():
                v.close()
        os._exit(0)
