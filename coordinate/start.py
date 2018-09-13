# coding=utf-8
import sys

sys.path.append('/root/server/server')

if __name__ == '__main__':
    from core import config

    config.init("/root/server/server/conf/pyg.conf")

    import core.globalvar as gl

    gl.init()

    from coordinate.server import Server

    # config.init("/home/pengyi/server/conf/pyg.conf")
    Server.start()
