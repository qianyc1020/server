# coding=utf-8
import os
import threading
import traceback

import core.globalvar as gl
from robot.client import Client
from utils.logger_utils import LoggerUtils
from utils.redis_utils import RedisUtils
from utils.stringutils import StringUtils


class Server(object):

    @staticmethod
    def start():
        try:
            gl.set_v("serverlogger", LoggerUtils("robot"))
            gl.set_v("redis", RedisUtils())
            accounts = []
            for i in range(0, 20):
                accounts.append("138000" + StringUtils.randomNum(4))
            for a in accounts:
                threading.Thread(target=Client.execute, args=(Client(a, 7),), name='robot').start()
        except:
            print traceback.print_exc()
            os._exit(0)
