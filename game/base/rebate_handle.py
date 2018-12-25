# coding=utf-8
import json
import traceback
from Queue import Empty

import core.globalvar as gl
from core import config
from utils.http_utils import HttpUtils


class RebateHandle(object):

    def __init__(self):
        self.__close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                rebates = queue.getall(20, True, 20)
                for rebate in rebates:
                    js = "["
                    for r in rebate:
                        js += json.dumps(r.__dict__)
                        js += ","
                    js += "]"
                    js = js.replace(",]", "]")
                    reqdata = {'jsonArray': js}
                    HttpUtils(config.get("api", "api_host")).post(config.get("api", "consumption_url"), reqdata)
            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
