# coding=utf-8
import pkgutil

from core import config
import core.globalvar as gl

config.init("/root/game/pyg.conf")
# config.init("/home/pengyi/server/server/conf/pyg.conf")
# config.init("C:\\Users\pengyi\server\conf\pyg.conf")
# config.init("/Users/yi/server/conf/pyg.conf")
gl.init()

from coordinate.server import Server

if __name__ == '__main__':
    Server.start()
    # loginserver = ReqLoginServer()
    # loginserver.account = "qqq"
    # loginserver.sex = 1
    # loginserver.nick = "wwoo"
    # loginserver.headUrl = "http://ss"
    # login.login(loginserver, "127.0.0.1:25225")
