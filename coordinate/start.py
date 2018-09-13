# coding=utf-8
import sys

sys.path.append('/root/server/server')

from gateway.server import Server
from core import config

if __name__ == '__main__':
    config.init("/root/server/server/conf/pyg.conf")
    # config.init("/home/pengyi/server/conf/pyg.conf")
    Server.start()
