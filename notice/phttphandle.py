# -*- coding:utf-8 -*-
import random
from decimal import Decimal

from core import config
import core.globalvar as gl

# 返回码
from data.database import data_account, data_gold
from protocol.base.base_pb2 import GAME_UPDATE_CURRENCY, NetMessage, RecUpdateCurrency, UPDATE_CURRENCY, LOGIN_SVR, \
    CHANGE_ONLINE
from protocol.base.game_base_pb2 import ReqUpdatePlayerOnline
from protocol.base.gateway_pb2 import GateWayMessage
from protocol.base.server_to_game_pb2 import RUNNING
from utils.stringutils import StringUtils
from utils.tcp_count import TcpCount


class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"


# 将字典转成字符串
def dict2str(d):
    s = ''
    for i in d:
        s = s + i + ': ' + d[i] + '\r\n'
    return s


class HttpRequest(object):

    def __init__(self):
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''
        self.session = None
        self.__redis = gl.get_v("redis")

    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        self.protocol = header_list[2]

    def passRequestHead(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val

    def passRequest(self, request):
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]  # 头部信息
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)

        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('&')  # 每一行是一个字段
            gl.get_v("serverlogger").logger.info("参数%s" % str(request_body))
            for i in parameters:
                if i == '':
                    continue
                key, val = i.split('=', 1)
                self.request_data[key] = val
        if self.method == 'GET':
            if self.url.find('?') != -1:  # 含有参数的get
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                parameters = req.split('&')
                gl.get_v("serverlogger").logger.info("参数%s" % str(req))
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val
                self.url = s_url
        self.do(self.url)

    def do(self, path):
        self.response_line = ErrorCode.NOT_FOUND
        self.response_body = "error"
        self.response_head['Content-Type'] = 'text/html'
        gl.get_v("serverlogger").logger.info("路径%s" % str(path))
        if path == "/addgold":
            userId = self.request_data["userId"]
            gold = self.request_data["gold"]
            type = self.request_data["type"]
            pwd = self.request_data["pwd"]
            if pwd == StringUtils.md5(userId + gold + type):
                data_account.update_currency(None, int(gold), 0, 0, 0, int(userId))
                data_gold.create_gold(int(type), int(userId), int(userId), int(gold))
                self.update_currency(int(userId))
                if self.__redis.exists(str(userId) + "_room"):
                    roomNo = self.__redis.get(str(userId) + "_room")
                    gameId = self.__redis.get(str(roomNo) + "_gameId")
                    games = gl.get_v("games")
                    random.shuffle(games)
                    for g in games:
                        if g.alloc_id == gameId and g.state == RUNNING:
                            self.sendToGame(g.uuid, GAME_UPDATE_CURRENCY, None)
                            break
                self.response_line = ErrorCode.OK
                self.response_body = "ok"

        elif path == "/enable":
            userId = self.request_data["userId"]
            enable = self.request_data["enable"]
            pwd = self.request_data["pwd"]
            if pwd == StringUtils.md5(userId + enable):
                if enable == "false":
                    self.send_to_gateway(LOGIN_SVR, None, int(userId))

                if self.__redis.exists(str(userId) + "_room"):
                    online = ReqUpdatePlayerOnline()
                    online.state = enable == "true"
                    roomNo = self.__redis.get(str(userId) + "_room")
                    gameId = self.__redis.get(str(roomNo) + "_gameId")
                    games = gl.get_v("games")
                    random.shuffle(games)
                    for g in games:
                        if g.alloc_id == gameId and g.state == RUNNING:
                            self.sendToGame(g.uuid, CHANGE_ONLINE, online)
                            break
                self.response_line = ErrorCode.OK
                self.response_body = "ok"
        elif path == "/online":
            gameuser = self.__redis.keys("*_room")
            connectuser = TcpCount().get_connect(config.get("gateway", "port"))
            self.response_line = ErrorCode.OK
            self.response_body = str(len(gameuser)) + "," + str(connectuser)

    def getResponse(self):
        response = self.response_line + dict2str(self.response_head) + '\r\n' + self.response_body
        gl.get_v("serverlogger").logger.info("返回%s" % response)
        return response

    def sendToGame(self, uuid, opcode, data):
        message = NetMessage()
        message.opcode = opcode
        if data is not None:
            message.data = data.SerializeToString()
        gl.get_v("serverlogger").logger.info("发送%d给游戏服" % opcode)
        gl.get_v("redis").publish(uuid, message.SerializeToString())

    def update_currency(self, userId):
        account = data_account.query_account_by_id(None, userId)
        if None is not account:
            currency = RecUpdateCurrency()
            currency.currency = int(account.gold.quantize(Decimal('0')))
            currency.gold = int(account.gold.quantize(Decimal('0')))
            currency.integral = int(account.integral.quantize(Decimal('0')))
            self.send_to_gateway(UPDATE_CURRENCY, currency, userId)

    def send_to_gateway(self, opcode, data, userId):
        send_data = NetMessage()
        send_data.opcode = opcode
        if data is not None:
            send_data.data = data.SerializeToString()

        s = GateWayMessage()
        s.userId = userId
        s.data = send_data.SerializeToString()
        gl.get_v("redis").publish("server-gateway", s.SerializeToString())
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, userId))
