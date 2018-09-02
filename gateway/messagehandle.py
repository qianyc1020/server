# coding=utf-8
class MessageHandle(object):
    __close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            message = queue.get(True, 20)
            if message is not None:
