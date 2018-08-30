# coding=utf-8
import socket
import threading
import time

import connect.client

if __name__ == '__main__':
    ip_port = ('127.0.0.1', 8888)
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    while True:
        t = time.time()
        nano = int(round(t * 1000000000))

        reload(connect.client)
        from connect.client import Client

        t = time.time()
        print(int(round(t * 1000000000)) - nano)

        conn, address = sk.accept()
        t = threading.Thread(target=Client.receive, args=(Client(), conn,), name='client')  # 线程对象.
        t.start()
