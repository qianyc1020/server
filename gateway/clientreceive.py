# coding=utf-8
import Queue
import re
import socket
import struct
import threading
import time
import traceback
from decimal import Decimal

import core.globalvar as gl
from core import config
from data.database import data_account
from data.database.data_account import update_login_with_info, update_login
from gateway.messagehandle import MessageHandle
from protocol.base.base_pb2 import *
from protocol.base.game_base_pb2 import ReqUpdatePlayerOnline
from utils.TestQueue import TestQueue
from utils.http_utils import HttpUtils
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
        self.sendQueue = TestQueue()
        self._close = False
        threading.Thread(target=self.relSend, name="clientsend").start()
        self.logining = False
        self.times = 0
        self.ttime = int(time.time())
        self.redis = gl.get_v("redis")

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
                md5bytes = self.readStringBytes(conn)
                length -= len(md5bytes) + 4
                result = self.readBytes(conn, length)
                if length == len(result) and 0 != len(result):
                    md5result = StringUtils.md5(self.newmd5keyBytes + result)
                    if md5bytes.decode("utf-8") == md5result:
                        data = NetMessage()
                        data.ParseFromString(result)
                        gl.get_v("serverlogger").logger.info('''收到%d''' % data.opcode)
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
                        elif data.opcode == SEND_CODE:
                            reqSendCode = ReqSendCode()
                            reqSendCode.ParseFromString(data.data)
                            recSendCode = RecSendCode()
                            if not re.match(r"^1[35678]\d{9}$", reqSendCode.phone):
                                recSendCode.state = 3
                            elif self.redis.exists(reqSendCode.phone + "_code"):
                                recSendCode.state = 2
                            else:
                                s = HttpUtils(config.get("api", "api_host")).get(
                                    config.get("api", "send_code_url") % reqSendCode.phone, None)
                                res = s.read()
                                recSendCode.state = 1
                            self.send_data(SEND_CODE, recSendCode)
                        else:
                            if self.userId is not None:
                                self.messageQueue.put(data)
                    else:
                        close = True
                        gl.get_v("serverlogger").logger.info("MD5 validation failed")
                else:
                    close = True
                    gl.get_v("serverlogger").logger.info("client close")

        except socket.error, e:
            print traceback.print_exc()
            gl.get_v("serverlogger").logger.info(e)
        except:
            print traceback.print_exc()
        finally:
            self.close()

    def close(self):
        if self.logining:
            self.logining = False
            return
        if self._close:
            return
        self._close = True
        if self.messageHandle is not None:
            if self.redis.exists(str(self.userId) + "_room"):
                online = ReqUpdatePlayerOnline()
                online.state = False
                data = NetMessage()
                data.opcode = CHANGE_ONLINE
                data.data = online.SerializeToString()
                self.messageQueue.put(data)
            self.messageHandle.close()
        try:
            if self.conns is not None:
                self.conns.shutdown(socket.SHUT_RDWR)
                self.conns.close()
        except:
            print traceback.print_exc()
        if self.userId is not None and self.userId in gl.get_v("clients") and gl.get_v("clients")[self.userId] == self:
            del gl.get_v("clients")[self.userId]
        gl.get_v("serverlogger").logger.info("client close")

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

    def write(self, data):
        datalen = struct.pack(">i", len(data))
        self.conns.sendall(datalen)
        self.conns.sendall(data)

    def relSend(self):
        while not self._close:
            try:
                datas = self.sendQueue.getall(20, True, 20)
                for data in datas:
                    md5str = StringUtils.md5(self.newmd5keyBytes + data)
                    md5bytes = md5str.decode("utf-8")
                    datalen = struct.pack(">i", len(data) + len(md5bytes) + 4)
                    self.conns.sendall(datalen)
                    self.write(md5bytes)
                    self.conns.sendall(data)
            except Queue.Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()

    def check_and_send(self, data):
        if len(data) > 0:
            netMessage = NetMessage()
            netMessage.ParseFromString(data)
            if netMessage.opcode == LOGIN_SVR:
                self.close()
            else:
                gl.get_v("serverlogger").logger.info(
                    "转发%d消息给%d" % (netMessage.opcode, 0 if self.userId is None else self.userId))
                self.sendQueue.put(data)

    def send(self, data):
        if len(data) > 0:
            self.sendQueue.put(data)

    def send_data(self, opcode, data):
        gl.get_v("serverlogger").logger.info("发送%d给%s" % (opcode, self.userId))
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
        username = re.compile(r"^[a-zA-Z0-9_-]\w{1,32}")
        if not username.match(loginserver.account):
            self.close()
            return
        account = data_account.login(loginserver, self.address)
        if account is not None:
            if self.checkLogin(account, loginserver.cls, False, loginserver.password, loginserver.device):
                t = time.time()
                if loginserver.nick is not None:
                    update_login_with_info(t, None, loginserver, self.address, loginserver.device)
                else:
                    update_login(t, None, self.address, loginserver.account, loginserver.device)
            if account.last_time == account.create_time:
                s = HttpUtils(config.get("api", "api_host")).get(
                    config.get("api", "send_code_url") % (self.userId, account.higher, self.address.split(':')[0]),
                    None)
                res = s.read()
        else:
            self.close()
            gl.get_v("serverlogger").logger.info("login fail")

    def checkLogin(self, account, cls, relogin, pwd, device):

        reclogin = RecLoginServer()
        if account is not None:
            if 1 == account.account_state:
                reclogin.state = LIMIT
            elif cls == OFFICIAL and not relogin:
                if device == account.device:
                    if self.redis.exists(account.account_name + "_session"):
                        session = self.redis.get(account.account_name + "_session")
                        if StringUtils.md5(session) == pwd:
                            self.loginSuccess(reclogin, account)
                            return True
                if self.redis.exists(account.account_name + "_code"):
                    code = self.redis.get(account.account_name + "_code")
                    if StringUtils.md5(str(code)) != pwd:
                        reclogin.state = CODE_ERROR
                    else:
                        self.redis.delobj(account.account_name + "_code")
                        self.loginSuccess(reclogin, account)
                        return True
                else:
                    reclogin.state = NO_CODE
            elif cls != OFFICIAL and account.pswd != pwd:
                reclogin.state = PASSWORD_ERROR
            else:
                self.loginSuccess(reclogin, account)
                return True
        else:
            reclogin.state = NO_ACCOUNT
        self.send_data(LOGIN_SVR, reclogin)
        return False

    def loginSuccess(self, reclogin, account):
        session = StringUtils.randomStr(32)
        self.redis.setexo(account.account_name + "_session", session, 604800)
        reclogin.session = session
        self.send_data(LOGIN_SVR, reclogin)
        self.userId = account.id
        if self.userId in gl.get_v("clients"):
            gl.get_v("clients")[self.userId].close()
        gl.get_v("clients")[self.userId] = self
        self.messageQueue = TestQueue()
        self.messageHandle = MessageHandle(self.userId)
        threading.Thread(target=MessageHandle.handle, args=(self.messageHandle, self.messageQueue,),
                         name='handle').start()  # 线程对象.
        if self.redis.exists(str(self.userId) + "_room"):
            online = ReqUpdatePlayerOnline()
            online.state = True
            data = NetMessage()
            data.opcode = CHANGE_ONLINE
            data.data = online.SerializeToString()
            self.messageQueue.put(data)
        self.update_user_info(account)
        self.update_currency(account)

        data = NetMessage()
        data.opcode = LOGIN_SVR
        self.messageQueue.put(data)
        self.logining = True

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
        username = re.compile(r"^[a-zA-Z0-9_-]\w{1,32}")
        if not username.match(relogin.account):
            self.close()
            return
        account = data_account.relogin(relogin, self.address)
        if account is not None:
            self.checkLogin(account, relogin.cls, True, relogin.password)
        else:
            self.close()
            gl.get_v("serverlogger").logger.info("login fail")
