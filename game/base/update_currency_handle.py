# coding=utf-8
import httplib
import json
import traceback
import urllib
from Queue import Empty

import core.globalvar as gl
from data.database import data_account, data_gold


class UpdateCurrencyHandle(object):

    def __init__(self):
        self.__close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                updates = queue.getall(20, True, 20)
                data_account.update_currencys(updates)
                data_gold.create_golds(1, updates)
            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
