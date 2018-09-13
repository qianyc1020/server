# coding=utf-8
import Queue
import socket
import struct
import threading

import core.globalvar as gl
from gateway import login
from core import config
from gateway.messagehandle import MessageHandle
from protocol.base import base_pb2
from protocol.base.base_pb2 import *
from utils.stringutils import StringUtils


class ClientReceive(object):
    conns = None
    address = None
    userId = None
    oldmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
    randomKey = None
    newmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
    messageQueue = None
    messageHandle = None

    def receive(self, conn, address):
        """
        : 接收
        :param conn:
        :param address:
        :return:
        """
        close = False
        self.conns = conn
        self.address = address

        self.randomKey = [StringUtils.randomStr(32), StringUtils.randomStr(32), StringUtils.randomStr(32),
                          StringUtils.randomStr(32), StringUtils.randomStr(32), StringUtils.randomStr(32),
                          StringUtils.randomStr(32), StringUtils.randomStr(32), StringUtils.randomStr(32),
                          StringUtils.randomStr(32)]

        checkversion = RecCheckVersion()
        checkversion.keys.extend(self.randomKey)
        gameinfo = checkversion.games.add()
        gameinfo.allocId = 1
        gameinfo.version = 10000
        self.send_data(NetMessage.CHECK_VERSION, checkversion.SerializeToString())

        try:
            while not close:
                length = self.readInt(conn)
                md5bytes = self.readStringBytes(conn)
                length -= len(md5bytes) + 4
                result = self.readBytes(conn, length)
                if length == len(result) and 0 != len(result):
                    md5result = StringUtils.md5(self.newmd5keyBytes + result)
                    if md5bytes.decode("utf-8") == md5result:
                        data = NetMessage()
                        data.ParseFromString(result)
                        gl.get_v("serverlogger").logger('''收到%d''' % data.opcode)
                        if data.opcode == data.CHECK_VERSION:
                            checkversion = ReqCheckVersion()
                            gl.get_v("serverlogger").logger('''老key%s''' % self.oldmd5keyBytes)
                            gl.get_v("serverlogger").logger('''选的key%s''' % self.randomKey[checkversion.keyIndex])
                            self.newmd5keyBytes = StringUtils.md5(self.oldmd5keyBytes.decode("utf-8") + "+" +
                                                                  self.randomKey[checkversion.keyIndex])
                            gl.get_v("serverlogger").logger('''新key%s''' % self.newmd5keyBytes)
                            noticelogin = RecNoticeLogin()
                            self.send_data(NetMessage.NOTICE_LOGIN, noticelogin.SerializeToString())
                        elif data.opcode == data.LOGIN_SVR:
                            self.login(data)
                        elif data.opcode == data.RELOGIN_SVR:
                            self.relogin(data)
                        else:
                            if self.userId is not None:
                                self.messageQueue.put(data)
                    else:
                        close = True
                        gl.get_v("serverlogger").logger("MD5 validation failed")
                else:
                    close = True
                    gl.get_v("serverlogger").logger("client close")

        except socket.error, e:
            gl.get_v("serverlogger").logger(e)
        except BaseException, x:
            gl.get_v("serverlogger").logger(x)
        finally:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            self.messageHandle.close()
            if self.userId is not None:
                del gl.get_v("clients")[self.userId]
            gl.get_v("serverlogger").logger("client close")

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
                gl.get_v("serverlogger").logger("client close")
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
                gl.get_v("serverlogger").logger("client close")
                break
        return result

    def write(self, data):
        datalen = struct.pack(">i", len(data))
        self.conns.sendall(datalen)
        self.conns.sendall(data)

    def send(self, data):
        if len(data) > 0:
            md5str = StringUtils.md5(self.newmd5keyBytes + data)
            md5bytes = md5str.decode("utf-8")
            datalen = struct.pack(">i", len(data) + len(md5bytes) + 4)
            self.conns.sendall(datalen)
            self.write(md5bytes)
            self.conns.sendall(data)

    def send_data(self, opcode, data):
        send_data = NetMessage()
        send_data.opcode = opcode
        send_data.data = data
        self.send(send_data.SerializeToString())

    def login(self, data):

        loginserver = ReqLoginServer()
        loginserver.ParseFromString(data.data)

        account = login.login(loginserver, self.address)
        if account is not None:
            self.checkLogin(account)
        else:
            self.conns.shutdown(socket.SHUT_RDWR)
            self.conns.close()
            gl.get_v("serverlogger").logger("login fail")

    def checkLogin(self, account):

        reclogin = RecLoginServer()
        if account is not None:
            if StringUtils.md5(account.account_name) != account.pswd:
                reclogin.state = base_pb2.PASSWORD_ERROR
            elif 1 == account.account_state:
                reclogin.state = base_pb2.LIMIT
            else:
                self.send_data(NetMessage.LOGIN_SVR, reclogin.SerializeToString())
                self.userId = account.id
                gl.get_v("clients")[self.userId] = self
                self.messageQueue = Queue.Queue()
                self.messageHandle = MessageHandle(self.userId)
                t = threading.Thread(target=MessageHandle.handle, args=(self.messageHandle, self.messageQueue,),
                                     name='handle')  # 线程对象.
                t.start()
                self.update_user_info(account)
                self.update_currency(account)
                return
        else:
            reclogin.state = base_pb2.ERROR
        self.send_data(NetMessage.LOGIN_SVR, reclogin.SerializeToString())

    def update_user_info(self, account):
        user_info = RecUserInfo()
        user_info.fristIn = account.create_time == account.last_time
        user_info.playerId = account.id
        user_info.account = account.account_name
        user_info.nick = account.nick_name
        user_info.headUrl = account.head_url
        user_info.sex = account.sex
        user_info.rootPower = account.authority
        user_info.registerTime = account.create_time
        user_info.playTotal = account.total_count
        user_info.registerTime = account.create_time
        user_info.introduce = account.integral
        user_info.phone = account.phone
        user_info.consumeVip = account.level
        user_info.consumeVal = account.experience
        # TODO 游戏中
        # user_info.allocId = account.id
        # user_info.gameId = account.id
        # user_info.isContest = account.id
        self.send_data(NetMessage.UPDATE_USER_INFO, user_info.SerializeToString())

    def update_currency(self, account):
        currency = RecUpdateCurrency()
        currency.currency = account.gold
        currency.gold = account.gold
        currency.integral = account.integral
        self.send_data(NetMessage.UPDATE_CURRENCY, currency.SerializeToString())

    def relogin(self, data):
        relogin = ReqRelogin()
        relogin.ParseFromString(data.data)

        account = login.relogin(relogin, self.address)
        if account is not None:
            self.checkLogin(account)
        else:
            self.conns.shutdown(socket.SHUT_RDWR)
            self.conns.close()
            gl.get_v("serverlogger").logger("login fail")
