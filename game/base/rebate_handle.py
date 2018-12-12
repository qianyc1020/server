# coding=utf-8
import httplib
import json
import traceback
import urllib
from Queue import Empty

import core.globalvar as gl


class RebateHandle(object):

    def __init__(self):
        self.__close = False
        self.reqheaders = {'Content-type': 'application/x-www-form-urlencoded',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Host': 'scan.3gzy3.cn',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1', }

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                rebate = queue.get(True, 20)
                js = "["
                for r in rebate:
                    js += json.dumps(r.__dict__)
                    js += ","
                js += "]"
                js = js.replace(",]", "]")
                reqdata = {'jsonArray': js}
                data = urllib.urlencode(reqdata)
                conn = httplib.HTTPConnection('scan.3gzy3.cn')
                conn.request('POST', '/user/consumption', data, self.reqheaders)
                res = conn.getresponse()

            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
