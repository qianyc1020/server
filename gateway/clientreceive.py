# coding=utf-8
import Queue
import socket
import struct
import threading

import gateway.globalvar as gl
from gateway.messagehandle import MessageHandle
from protocol.base.base_pb2 import *
from utils.stringutils import StringUtils


class ClientReceive(object):
    conns = None
    userId = None
    oldmd5keyBytes = "2704031cd4814eb2a82e47bd1d9042c6".encode("utf-8")
    randomKey = None
    newmd5keyBytes = "2704031cd4814eb2a82e47bd1d9042c6".encode("utf-8")

    def receive(self, conn):
        """
        : 接收
        :param conn:
        :return:
        """
        close = False
        self.conns = conn
        messageQueue = None
        messageHandle = None

        self.randomKey = [StringUtils.randomStr(32), StringUtils.randomStr(32), StringUtils.randomStr(32),
                          StringUtils.randomStr(32), StringUtils.randomStr(32), StringUtils.randomStr(32),
                          StringUtils.randomStr(32), StringUtils.randomStr(32), StringUtils.randomStr(32),
                          StringUtils.randomStr(32)]

        data = NetMessage()
        data.opcode = data.CHECK_VERSION
        checkversion = RecCheckVersion()
        checkversion.keys.extend([self.randomKey])
        gameinfo = checkversion.games.add()
        gameinfo.allocId = 1
        gameinfo.version = 10000
        data.data = checkversion.SerializeToString()
        self.send(data.SerializeToString())

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
                        print (data.opcode)
                        if data.opcode == NetMessage.Opcode.CHECK_VERSION:
                            checkversion = ReqCheckVersion()
                            newmd5keyBytes = StringUtils.md5(
                                self.randomKey[checkversion.keyIndex] + self.oldmd5keyBytes.decode("utf-8"))
                            print newmd5keyBytes
                        elif data.opcode == data.LOGIN_SVR:
                            loginserver = ReqLoginServer()
                            loginserver.ParseFromString(data.data)

                            # TODO userId
                            self.userId = 10010

                            gl.get_v("clients")[self.userId] = self

                            messageQueue = Queue.Queue()
                            messageHandle = MessageHandle(self.userId)
                            t = threading.Thread(target=MessageHandle.handle, args=(messageHandle, messageQueue,),
                                                 name='handle')  # 线程对象.
                            t.start()
                        else:
                            if self.userId is not None:
                                messageQueue.put(data)
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
            messageHandle.close()
            if self.userId is not None:
                del gl.get_v("clients")[self.userId]
            gl.get_v("serverlogger").logger("client close")

    def readInt(self, conn):
        msg1 = conn.recv(1)  # total data length
        msg2 = conn.recv(1)  # total data length
        msg3 = conn.recv(1)  # total data length
        msg4 = conn.recv(1)  # total data length
        data = struct.unpack("i", msg4 + msg3 + msg2 + msg1)
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
            b = bytearray()
            b.append(datalen[0])
            self.conns.sendall(b)
            b.remove(datalen[0])
            b.append(datalen[1])
            self.conns.sendall(b)
            b.remove(datalen[1])
            b.append(datalen[2])
            self.conns.sendall(b)
            b.remove(datalen[2])
            b.append(datalen[3])
            self.conns.sendall(b)
            self.write(md5bytes)
            self.conns.sendall(data)
