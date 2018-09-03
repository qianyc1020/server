# coding=utf-8
import Queue
import socket
import struct
import threading

from gateway.messagehandle import MessageHandle
from protocol.base.base_pb2 import *
from utils.stringutils import StringUtils

clients = {}


class ClientReceive(object):
    conns = None
    name = ''
    oldmd5keyBytes = "2704031cd4814eb2a82e47bd1d9042c6".encode("utf-8")
    randomKey = None
    newmd5keyBytes = "2704031cd4814eb2a82e47bd1d9042c6".encode("utf-8")
    def receive(self, conn):
        """
        : 接收
        :param conn:
        :return:
        """
        name = ""
        close = False
        self.conns = conn
        messageQueue = Queue.Queue()
        messageHandle = MessageHandle()
        t = threading.Thread(target=MessageHandle.handle, args=(messageHandle, messageQueue,), name='handle')  # 线程对象.
        t.start()
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
                        data.ParseFromString(result.decode("utf-8"))
                        if data.opcode == NetMessage.Opcode.CHECK_VERSION:
                            self.randomKey = StringUtils.randomStr(32)
                            checkversion = ReqCheckVersion()
                            gameinfo = ReqCheckVersion.GameInfo()
                            gameinfo.allocId = 1
                            gameinfo.version = 10000
                            checkversion.games = gameinfo
                            checkversion.keys = self.randomKey
                            self.send(checkversion.SerializeToString())
                        elif data.opcode == NetMessage.Opcode.LOGIN_SVR:
                            loginserver = ReqLoginServer()
                            loginserver.ParseFromString(data.data)
                        else:
                            messageQueue.put(data)
                    else:
                        close = True
                        print "md5验证失败"
                else:
                    close = True
                    print "client close"

        except socket.error, e:
            print e
        except BaseException, x:
            print x
        finally:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            messageHandle.close()
            print "over"

    def readInt(self, conn):
        msg = conn.recv(4)  # total data length
        if len(msg) <= 0:  # 接收空数据包
            return 0
        data = struct.unpack("i", msg)
        return data[0]

    def readStringBytes(self, conn):
        length = self.readInt(conn)
        result = bytes()
        while length != 0:
            result1 = conn.recv(length)
            if result1:
                result += result1
                length -= len(result1)
        return result

    def readBytes(self, conn, length):
        result = bytes()
        while length != 0:
            result1 = conn.recv(length)
            if result1:
                result += result1
                length -= len(result1)
            else:
                print "client close"
                break
        return result

    def write(self, data):
        datalen = struct.pack("i", len(data))
        self.conns.sendall(datalen)
        self.conns.sendall(data)

    def send(self, data):
        if len(data) > 0:
            md5str = StringUtils.md5(self.newmd5keyBytes + data)
            md5bytes = md5str.decode("utf-8")
            datalen = struct.pack("i", len(data) + len(md5bytes) + 4)
            self.conns.sendall(datalen)
            self.write(md5bytes)
            self.conns.sendall(data)
