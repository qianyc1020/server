# coding=utf-8

import sys

sys.path.append('/root/server/server')
from gateway.server import Server

if __name__ == '__main__':
    Server.start()
