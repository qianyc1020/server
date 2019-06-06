# coding=utf-8
import os
import traceback

import core.globalvar as gl
from utils.logger_utils import LoggerUtils
from utils.redis_utils import RedisUtils


class Server(object):

    @staticmethod
    def start():
        try:
            gl.set_v("serverlogger", LoggerUtils("robot"))
            gl.set_v("redis", RedisUtils())
            account = ["13800138000", "18983358480"]
            for a in account:

        except:
            print traceback.print_exc()
            os._exit(0)
