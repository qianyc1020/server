# coding=utf-8
import sys

from core import config

sys.path.append('/root/server/server')
from gateway.server import Server

if __name__ == '__main__':
    config.init("/root/server/server/conf/pyg.conf")
    # config.init("/home/pengyi/server/conf/pyg.conf")
    Server.start()
    # config.init("/home/pengyi/server/conf/pyg.conf")
    # loginserver = ReqLoginServer()
    # loginserver.account = "qqq"
    # loginserver.sex = 1
    # loginserver.nick = "wwoo"
    # loginserver.headUrl = "http://ss"
    # login.login(loginserver, "127.0.0.1:25225")
