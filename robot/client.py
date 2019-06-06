# coding=utf-8
import random
import socket
import struct
import time

import core.globalvar as gl
from core import config
from protocol.base.base_pb2 import *
from utils.stringutils import StringUtils


class Client(object):

    def __init__(self, account, redis):
        self.account = account
        self.ip_port = ('127.0.0.1', 9999)
        self.s = socket.socket()
        self.s.connect(self.ip_port)
        self.oldmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
        self.newmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
        self.redis = redis

    def execute(self):
        while True:
            length = self.readInt(self.s)
            ttime = int(time.time())
            if ttime == self.ttime:
                self.times += 1
                if self.times == 25:
                    break
            else:
                self.times = 0
                self.ttime = ttime
            if length > 102400:
                gl.get_v("serverlogger").logger.info("packet length more than 100kb")
                break
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
                    elif data.opcode == CHECK_VERSION:

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
        self.redis.setex(self.account + "_code", int(code), 10)
        loginserver = ReqLoginServer()
        loginserver.account = self.account
        loginserver.password = StringUtils.md5(code)
        loginserver.cls = OFFICIAL
        self.send_data(LOGIN_SVR, loginserver)
