# -*- coding=utf-8 -*-
import socket
import threading
import traceback
from Queue import Queue

import core.globalvar as gl
from core import config

from phttphandle import HttpRequest


# 每个任务线程
from utils.tcp_count import TcpCount


class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super(WorkThread, self).__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger:
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = Queue()
        for i in range(self.thread_number):  # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


def tcp_link(sock, addr):
    gl.get_v("serverlogger").logger.info('Accept new connection from %s:%s...' % addr)
    request = sock.recv(1024)
    http_req = HttpRequest()
    try:
        http_req.passRequest(request)
    except:
        print traceback.print_exc()
    sock.send(http_req.getResponse().encode('utf-8'))
    sock.close()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(config.get("coordinate", "http_port"))))
    s.listen(10)
    thread_pool = ThreadPoolManger(5)
    while True:
        sock, addr = s.accept()
        thread_pool.add_work(tcp_link, *(sock, addr))


if __name__ == '__main__':
    p = TcpCount().get_info(10001)
    print p
