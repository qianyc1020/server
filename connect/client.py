# coding=utf-8
import hashlib
import socket
import struct
from socket import _socketobject

clients = {}


class Client(object):
    conns = _socketobject()
    name = ''
    md5keyBytes = "2704031cd4814eb2a82e47bd1d9042c6".encode("utf-8")

    def receive(self, conn):
        """
        : 接收
        :param conn:
        :return:
        """
        name = ""
        close = False
        self.conns = conn
        try:
            while not close:
                length = self.readInt(conn)
                md5bytes = self.readStringBytes(conn)
                length -= len(md5bytes) + 4
                result = self.readBytes(conn, length)
                if length == len(result) and 0 != len(result):
                    h = hashlib.md5()
                    h.update(self.md5keyBytes + result)
                    if md5bytes.decode("utf-8") == h.hexdigest():
                        body = result.decode("utf-8")
                        print(body)
                        clients[body] = conn
                        self.send(result)
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
            h = hashlib.md5()
            h.update(self.md5keyBytes + data)
            md5bytes = h.hexdigest().decode("utf-8")
            datalen = struct.pack("i", len(data) + len(md5bytes) + 4)
            self.conns.sendall(datalen)
            self.write(md5bytes)
            self.conns.sendall(data)
