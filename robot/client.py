# coding=utf-8
import random
import socket
import struct
import threading
import traceback

import core.globalvar as gl
from core import config
from protocol.base.base_pb2 import *
from protocol.game.bairen_pb2 import BaiRenRecAsk
from protocol.service.match_pb2 import ReqApplyEnterMatch, RecApplyEnterMatch
from robot.betscore import BetScore
from utils.stringutils import StringUtils


class Client(object):

    def __init__(self, account, allocId):
        self.accountId = 0
        self.account = account
        self.ip_port = ('103.16.231.113', 10001)
        self.s = socket.socket()
        self.s.connect(self.ip_port)
        self.oldmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
        self.newmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
        # self.redis = gl.get_v("redis")
        self.allocId = allocId
        self.betScore = None

    def execute(self):
        while True:
            length = self.readInt(self.s)
            md5bytes = self.readStringBytes(self.s)
            length -= len(md5bytes) + 4
            result = self.readBytes(self.s, length)
            if length == len(result) and 0 != len(result):
                md5result = StringUtils.md5(self.newmd5keyBytes + result)
                if md5bytes.decode("utf-8") == md5result:
                    data = NetMessage()
                    data.ParseFromString(result)
                    gl.get_v("serverlogger").logger.info('''收到%d''' % data.opcode)
                    if data.opcode == CHECK_VERSION:
                        self.checkVersion(data)
                        self.login()
                    elif data.opcode == LOGIN_SVR:
                        recLoginServer = RecLoginServer()
                        recLoginServer.ParseFromString(data.data)
                        if recLoginServer.state == SUCCESS:
                            gl.get_v("serverlogger").logger.info("login success")
                        else:
                            gl.get_v("serverlogger").logger.info("login fail:" + str(recLoginServer.state))
                            self.close()
                            return
                    elif data.opcode == UPDATE_USER_INFO:
                        user_info = RecUserInfo()
                        user_info.ParseFromString(data.data)
                        if user_info.allocId != 0:
                            gl.get_v("serverlogger").logger.info("client close:allocId:" + str(user_info.allocId))
                            self.close()
                        else:
                            self.accountId = user_info.playerId
                            self.intoRoom()
                    elif data.opcode == APPLY_ENTER_MATCH:
                        recApplyEnterMatch = RecApplyEnterMatch()
                        recApplyEnterMatch.ParseFromString(data.data)
                        if recApplyEnterMatch.state != recApplyEnterMatch.SUCCESS:
                            gl.get_v("serverlogger").logger.info("enter match fail")
                            self.close()
                    elif data.opcode == ASK_ACTION:
                        gl.get_v("serverlogger").logger.info("start bet")
                        baiRenRecAsk = BaiRenRecAsk()
                        baiRenRecAsk.ParseFromString(data.data)
                        if baiRenRecAsk.type == 2:
                            self.betScore = BetScore(self)
                            threading.Thread(target=BetScore.execute, args=(self.betScore,), name='betScore').start()
                    elif data.opcode == SETTLE_GAME:
                        gl.get_v("serverlogger").logger.info("end bet")
                        if self.betScore is not None:
                            self.betScore.close()
                        self.betScore = None

    def readInt(self, conn):
        msg = conn.recv(4)  # total data length
        data = struct.unpack(">i", msg)
        return data[0]

    def readStringBytes(self, conn):
        length = self.readInt(conn)
        result = bytes()
        while length != 0:
            result1 = conn.recv(length)
            if result1:
                result += result1
                length -= len(result1)
            else:
                gl.get_v("serverlogger").logger.info("client close")
                break
        return result

    def readBytes(self, conn, length):
        result = bytes()
        while length != 0:
            result1 = conn.recv(length)
            if result1:
                result += result1
                length -= len(result1)
            else:
                gl.get_v("serverlogger").logger.info("client close")
                break
        return result

    def send_data(self, opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        if data is not None:
            send_data.data = data.SerializeToString()
        self.send(send_data.SerializeToString())

    def send(self, data):
        md5str = StringUtils.md5(self.newmd5keyBytes + data)
        md5bytes = md5str.decode("utf-8")
        datalen = struct.pack(">i", len(data) + len(md5bytes) + 4)
        self.s.sendall(datalen)
        self.write(md5bytes)
        self.s.sendall(data)

    def write(self, data):
        datalen = struct.pack(">i", len(data))
        self.s.sendall(datalen)
        self.s.sendall(data)

    def checkVersion(self, data):
        recCheckversion = RecCheckVersion()
        recCheckversion.ParseFromString(data.data)
        keyIndex = random.randint(0, len(recCheckversion.keys) - 1)
        checkversion = ReqCheckVersion()
        checkversion.keyIndex = keyIndex
        self.send_data(CHECK_VERSION, checkversion)
        self.newmd5keyBytes = StringUtils.md5(self.oldmd5keyBytes.decode("utf-8") + "+" +
                                              recCheckversion.keys[keyIndex])

    def login(self):
        code = StringUtils.randomNum(6)
        # self.redis.setex(self.account + "_code", int(code), 10)
        loginserver = ReqLoginServer()
        loginserver.account = self.account
        loginserver.nick = self.account
        loginserver.password = StringUtils.md5(self.account)
        loginserver.cls = WECHAT
        self.send_data(LOGIN_SVR, loginserver)

    def close(self):
        try:
            if self.s is not None:
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
        except:
            print traceback.print_exc()

    def intoRoom(self):
        reqApplyEnterMatch = ReqApplyEnterMatch()
        reqApplyEnterMatch.allocId = self.allocId
        reqApplyEnterMatch.level = 11
        self.send_data(APPLY_ENTER_MATCH, reqApplyEnterMatch)
