# coding=utf-8
import pkg_resources

from core import config
import core.globalvar as gl

config.init("/root/game/pyg.conf")
# config.init("/home/pengyi/server/server/conf/pyg.conf")
# config.init("C:\\Users\pengyi\server\conf\pyg.conf")
# config.init("/Users/yi/server/conf/pyg.conf")
gl.init()

from game.tuitongzi.server.server import Server

if __name__ == '__main__':
    Server.start()
