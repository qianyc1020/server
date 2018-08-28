# coding=utf-8

import tornado.ioloop
from nats.io import Client

from connect import nats1

nc = Client()


@tornado.gen.coroutine
def main():
    yield nc.connect(servers=["nats://pengyi:pengyi19960207@127.0.0.1:1111"], allow_reconnect=False)
    if nc.is_connected:
        future = nc.subscribe(subject="asas", cb=nats1.handler)
        sid = future.result()
        nc.publish("asas", "222")
        nc.publish("asas", "222")
        nc.publish("asas", "222")
        nc.publish("asas", "222")


if __name__ == '__main__':
    main()
    tornado.ioloop.IOLoop.instance().start()
