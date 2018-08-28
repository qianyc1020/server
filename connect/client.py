# coding=utf-8
import socket
import struct
from socket import _socketobject

clients = {}


class Client(object):
    conns = _socketobject()
    name = ''

    def receive(self, conn):
        """
        : 接收
        :param conn:
        :return:
        """
        name = ""
        close = False
        conns = conn
        try:
            while not close:
                length = self.readInt(conn)
                result = bytes()
                while length != 0:
                    result1 = conn.recv(length)
                    if result1:
                        result += result1
                        length -= len(result1)
                    else:
                        close = True
                        print "client close"
                        break
                if length == 0 and 0 != len(result):
                    print(result)
                    name = result.decode("utf-8")
                    clients[name] = conn
                    datalen = struct.pack("i", len(result))
                    conn.sendall(datalen)
                    conn.sendall(result)
                else:
                    close = True
                    print "client close"

        except socket.error, e:
            print e
        except BaseException, x:
            print x
        finally:
            del clients[name]
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            print "over"

    def readInt(self, conn):
        msg = conn.recv(4)  # total data length
        if len(msg) <= 0:  # 接收空数据包
            return 0
        data = struct.unpack("i", msg)
        return data[0]

    def send(self, data):
        if len(data) > 0:
            datalen = struct.pack("i", len(data))
            self.conns.sendall(datalen)
            self.conns.sendall(data)
