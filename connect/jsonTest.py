# coding=utf-8
from connect.logger_utils import LoggerUtils
from connect.redis_utils import RedisUtils


class Cli(object):
    def __init__(self, c, b):
        self.c = c
        self.b = b

    c = u"a"
    b = u"s"


if __name__ == '__main__':
    r = RedisUtils()
    ss = LoggerUtils("ss")
    ss.logger("ss")
    aa = LoggerUtils("aa")
    aa.logger("aa")
    ss.logger("ss")

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
