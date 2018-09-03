# coding=utf-8
import Queue
import socket
import threading

import gateway
import gateway.clientreceive
from gateway.serverreceive import ServerReceive
from utils.natsutils import NatsUtils

natsobj = None
serverqueue = None


def messagehandle(msg):
    serverqueue.put(msg.data)


class Server(object):

    @staticmethod
    def start():
        global natsobj
        global serverqueue

        serverqueue = Queue.Queue()
        natsobj = NatsUtils(["nats://pengyi:pengyi19960207@127.0.0.1:1111"], "server-gateway",
                            messagehandle)
        natsthread = threading.Thread(target=NatsUtils.startNats, args=(natsobj,), name='natsthread')
        natsthread.start()

        t = threading.Thread(target=ServerReceive.handle, args=(ServerReceive(), serverqueue,), name='handle')  # 线程对象.
        t.start()

        ip_port = ('127.0.0.1', 8888)
        sk = socket.socket()
        sk.bind(ip_port)
        sk.listen(5)
        while True:
            reload(gateway.clientreceive)
            from gateway.clientreceive import ClientReceive

            conn, address = sk.accept()
            t = threading.Thread(target=ClientReceive.receive, args=(ClientReceive(), conn,),
                                 name='clientreceive')  # 线程对象.
            t.start()
