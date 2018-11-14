# coding=utf-8
import sys

# sys.path.append('/root/server')
# sys.path.append('/home/pengyi/server/server')
# sys.path.append('C:\\Users\pengyi\server')
sys.path.append('/Users/yi/server')

from core import config
import core.globalvar as gl

config.init("/root/server/conf/pyg.conf")
# config.init("/home/pengyi/server/server/conf/pyg.conf")
# config.init("C:\\Users\pengyi\server\conf\pyg.conf")
# config.init("/Users/yi/server/conf/pyg.conf")
gl.init()

from gateway.server import Server

if __name__ == '__main__':
    Server.start()
    # config.init("/home/pengyi/server/conf/pyg.conf")
    # loginserver = ReqLoginServer()
    # loginserver.account = "qqq"
    # loginserver.sex = 1
    # loginserver.nick = "wwoo"
    # loginserver.headUrl = "http://ss"
    # login.login(loginserver, "127.0.0.1:25225")
