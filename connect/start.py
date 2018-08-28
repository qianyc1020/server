# coding=utf-8
import socket
import threading

from connect.client import Client

if __name__ == '__main__':
    ip_port = ('127.0.0.1', 8888)
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    while True:
        conn, address = sk.accept()
        t = threading.Thread(target=Client.receive, args=(Client(), conn,), name='client')  # 线程对象.
        t.start()
