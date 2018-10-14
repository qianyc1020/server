# coding=utf-8
import json

from core import config
import core.globalvar as gl
config.init("C:\\Users\pengyi\server\conf\pyg.conf")
gl.init()
from utils.redis_utils import RedisUtils


class Cli(object):
    def __init__(self, c, b):
        self.c = c
        self.b = b

    c = u"a"
    b = u"s"


if __name__ == '__main__':
    # r = RedisUtils()
    s = []
    s.append(1)
    s.append(2)
    ss = json.dumps(s)

    sss = json.loads(ss)
    # r.setobj("s", s)

    # g = r.getobj("s", list)
    print 1

    # cli = Cli("1", "2")
    #
    # r.setobj("obj1", cli)
    #
    #
    # def hh(h):
    #     return Cli(h['c'], h['b'])
    #
    #
    # c = r.getobj("obj1", hh)
    #
    # r.delobj("obj1")

    # print(c)
