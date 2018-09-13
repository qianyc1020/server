# coding=utf-8

import sys

from core import config

sys.path.append('/root/server/server')
from coordinate.server import Server

if __name__ == '__main__':
    config.init("/root/server/server/conf/pyg.conf")
    # config.init("/home/pengyi/server/conf/pyg.conf")
    Server.start()
