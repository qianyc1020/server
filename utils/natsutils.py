import tornado.ioloop
from nats.io import Client


class NatsUtils(object):
    __nc__ = Client()
    __handle__ = None
    __servers__ = None
    __subject__ = None

    def __init__(self, servers, subject, handle):
        self.__servers__ = servers
        self.__subject__ = subject
        self.__handle__ = handle

    @tornado.gen.coroutine
    def main(self):
        yield self.__nc__.connect(servers=self.__servers__, allow_reconnect=False)
        if self.__nc__.is_connected:
            future = self.__nc__.subscribe(self.__subject__, cb=self.__handle__)
            sid = future.result()

    def startNats(self):
        self.main()
        tornado.ioloop.IOLoop.instance().start()

    def publish(self, subject, data):
        if self.__nc__.is_connected:
            self.__nc__.publish(subject, data)
