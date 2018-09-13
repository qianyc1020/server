# coding=utf-8
import sys

sys.path.append('/root/server/server')

if __name__ == '__main__':
    from core import config

    config.init("/root/server/server/conf/pyg.conf")

    import core.globalvar as gl

    gl.init()

    from gateway.server import Server

    # config.init("/home/pengyi/server/conf/pyg.conf")
    Server.start()
    # config.init("/home/pengyi/server/conf/pyg.conf")
    # loginserver = ReqLoginServer()
    # loginserver.account = "qqq"
    # loginserver.sex = 1
    # loginserver.nick = "wwoo"
    # loginserver.headUrl = "http://ss"
    # login.login(loginserver, "127.0.0.1:25225")
