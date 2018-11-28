import tornado.ioloop
import tornado.gen
from nats.io import Client


class NatsUtils(object):

    def __init__(self, servers, subject, handle):
        self.__nc__ = Client()
        self.__servers__ = servers
        self.__subject__ = subject
        self.__handle__ = handle

    @tornado.gen.coroutine
    def main(self):
        yield self.__nc__.connect(self.__servers__)
        if self.__nc__.is_connected:
            for i in range(0, len(self.__subject__)):
                self.__nc__.subscribe(self.__subject__[i], cb=self.__handle__[i])

    def startNats(self):
        tornado.ioloop.IOLoop.current().run_sync(self.main)

    def publish(self, subject, data):
        if self.__nc__.is_connected:
            self.__nc__.publish(subject, data)

    def isConnect(self):
        return self.__nc__.is_connected
