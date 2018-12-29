import hashlib
import random


class StringUtils(object):

    @staticmethod
    def randomStr(length):
        seed = "1234567890abcdefghijklmnopqrstuvwxyz"
        sa = []
        for i in range(length):
            sa.append(random.choice(seed))
        return ''.join(sa)

    @staticmethod
    def md5(data):
        h = hashlib.md5()
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def phoneToNick(phone):
        if len(phone) > 8:
            return phone[:3] + "*****" + phone[-3:]
        else:
            return phone
