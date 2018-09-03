# coding=utf-8


class ServerReceive(object):
    __close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            message = queue.get(True, 20)
            print("[Received: {0}]".format(message))
