# coding=utf-8
import json
import time

import redis

from core import config


class RedisUtils(object):

    def __init__(self):
        self.__pool = redis.ConnectionPool(host=config.get("redis", "host"), port=int(config.get("redis", "port")),
                                           db=0)
        self.__redis = redis.Redis(connection_pool=self.__pool)

    def lock(self, key, timeout):
        """
        : 加锁
        :param key:
        :param timeout:
        :return:
        """
        t = time.time()
        nano = int(round(t * 1000000000))
        timeoutnanos = timeout * 1000000L
        while (int(round(time.time() * 1000000000)) - nano) < timeoutnanos:
            if self.__redis.setnx(key, time.strftime("%Y%m%d%H%M%S", time.localtime())) == 1:
                self.__redis.expire(key, 5)
                return True
            time.sleep(0.002)
        return False

    def unlock(self, key):
        """
        : 解锁
        :param key:
        :return:
        """
        self.__redis.delete(key)

    def setobj(self, key, obj):
        """
        : 存入对象
        :param key:
        :param obj:
        :return:
        """
        self.__redis.set(key, json.dumps(obj.__dict__))

    def set(self, key, obj):
        """
        : 存入数组
        :param key:
        :param obj:
        :return:
        """
        self.__redis.set(key, json.dumps(obj))

    def getobj(self, key, obj):
        """
        : 取出对象
        :param key:
        :param obj:
        :return:
        """
        loaded = json.loads(self.__redis.get(key))
        obj.__dict__ = loaded
        return obj

    def get(self, key):
        """
        : 取出数组
        :param key:
        :return:
        """
        return json.loads(self.__redis.get(key))

    def delobj(self, key):
        """
        : 删除对象
        :param key:
        :return:
        """
        self.__redis.delete(key)

    def exists(self, key):
        return self.__redis.exists(key)
