# coding=utf-8
import Queue
import socket
import threading

import gateway
import gateway.clientreceive
import gateway.globalvar as gl
from gateway.serverreceive import ServerReceive
from utils.logger_utils import LoggerUtils
from utils.natsutils import NatsUtils


def messagehandle(msg):
    gl.get_v("serverqueue").put(msg.data)


class Server(object):

    @staticmethod
    def start():
        gl.init()
        gl.set_v("serverlogger", LoggerUtils("gateway"))
        gl.set_v("serverqueue", Queue.Queue())
        gl.set_v("natsobj", NatsUtils(["nats://pengyi:pengyi19960207@127.0.0.1:1111"], "server-gateway", messagehandle))
        gl.set_v("clients", {})

        natsthread = threading.Thread(target=NatsUtils.startNats, args=(gl.get_v("natsobj"),), name='natsthread')
        natsthread.start()
        gl.get_v("serverlogger").logger("natsthread started")

        t = threading.Thread(target=ServerReceive.handle, args=(ServerReceive(), gl.get_v("serverqueue"),),
                             name='handle')
        t.start()
        gl.get_v("serverlogger").logger("serverqueue started")

        ip_port = ('', 8888)
        sk = socket.socket()
        sk.bind(ip_port)
        sk.listen(5)
        gl.get_v("serverlogger").logger("server started")
        while True:
            try:
                reload(gateway.clientreceive)
                from gateway.clientreceive import ClientReceive

                conn, address = sk.accept()
                t = threading.Thread(target=ClientReceive.receive, args=(ClientReceive(), conn,),
                                     name='clientreceive')  # 线程对象.
                t.start()
            except BaseException, e:
                print(e)
