# coding=utf-8
import pkg_resources

from core import config
import core.globalvar as gl

config.init("./conf/pyg.conf")
gl.init()

from game.niuniu.server.server import Server

if __name__ == '__main__':
    Server.start()
