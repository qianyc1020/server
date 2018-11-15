# coding=utf-8
import Queue
import socket
import struct
import threading
from decimal import Decimal

import core.globalvar as gl
from core import config
from data.database import data_account
from gateway.messagehandle import MessageHandle
from protocol.base.base_pb2 import *
from utils.stringutils import StringUtils


class ClientReceive(object):

    def __init__(self):
        self.conns = None
        self.address = None
        self.userId = None
        self.oldmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
        self.randomKey = None
        self.newmd5keyBytes = config.get("gateway", "md5").encode("utf-8")
        self.messageQueue = None
        self.messageHandle = None
        self.lock = threading.Lock()

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
        self.send_data(CHECK_VERSION, checkversion)

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
                        if data.opcode == CHECK_VERSION:
                            checkversion = ReqCheckVersion()
                            checkversion.ParseFromString(data.data)
                            self.newmd5keyBytes = StringUtils.md5(self.oldmd5keyBytes.decode("utf-8") + "+" +
                                                                  self.randomKey[checkversion.keyIndex])
                            noticelogin = RecNoticeLogin()
                            self.send_data(NOTICE_LOGIN, noticelogin)
                        elif data.opcode == LOGIN_SVR:
                            self.login(data)
                        elif data.opcode == RELOGIN_SVR:
                            self.relogin(data)
                        elif data.opcode == SEND_PING:
                            self.send_data(SEND_PING, None)
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
            print e
            gl.get_v("serverlogger").logger(e)
        except BaseException, x:
            print x
            gl.get_v("serverlogger").logger(x)
        finally:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            if self.messageHandle is not None:
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
        gl.get_v("serverlogger").logger("发送%d给%s" % (opcode, self.userId))
        self.lock.acquire()
        send_data = NetMessage()
        send_data.opcode = opcode
        if data is not None:
            send_data.data = data.SerializeToString()
        self.send(send_data.SerializeToString())
        self.lock.release()

    def login(self, data):

        loginserver = ReqLoginServer()
        loginserver.ParseFromString(data.data)

        account = data_account.login(loginserver, self.address)
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
                reclogin.state = PASSWORD_ERROR
            elif 1 == account.account_state:
                reclogin.state = LIMIT
            else:
                self.send_data(LOGIN_SVR, reclogin)
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
            reclogin.state = ERROR
        self.send_data(LOGIN_SVR, reclogin)

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
        if account.introduce is not None:
            user_info.introduce = account.introduce
        if account.phone is not None:
            user_info.phone = account.phone
        user_info.consumeVip = account.level
        user_info.consumeVal = account.experience
        redis = gl.get_v("redis")
        if redis.exists(str(self.userId) + "_room"):
            roomNo = redis.get(str(self.userId) + "_room")
            gameId = redis.get(str(roomNo) + "_gameId")
            user_info.allocId = gameId
            user_info.gameId = roomNo
        # user_info.isContest = account.id
        self.send_data(UPDATE_USER_INFO, user_info)

    def update_currency(self, account):
        currency = RecUpdateCurrency()
        currency.currency = int(account.gold.quantize(Decimal('0')))
        currency.gold = int(account.gold.quantize(Decimal('0')))
        currency.integral = int(account.integral.quantize(Decimal('0')))
        self.send_data(UPDATE_CURRENCY, currency)

    def relogin(self, data):
        relogin = ReqRelogin()
        relogin.ParseFromString(data.data)

        account = data_account.relogin(relogin, self.address)
        if account is not None:
            self.checkLogin(account)
        else:
            self.conns.shutdown(socket.SHUT_RDWR)
            self.conns.close()
            gl.get_v("serverlogger").logger("login fail")
