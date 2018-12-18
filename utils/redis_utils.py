# coding=utf-8
import cPickle
import json
import random
import threading
import time

import redis

import core.globalvar as gl
from core import config


class RedisUtils(object):

    def __init__(self):
        self.__pool = redis.ConnectionPool(host=config.get("redis", "host"), port=int(config.get("redis", "port")),
                                           db=0)
        self.__redis = redis.Redis(connection_pool=self.__pool)
        redis_ping = threading.Thread(target=self._ping, name="redis_ping")
        redis_ping.start()

    def lock(self, key):
        """
        : 加锁
        :param key:
        :return:
        """
        t = time.time()
        while True:
            if self.__redis.setnx(key, time.strftime("%Y%m%d%H%M%S", time.localtime())) == 1:
                self.__redis.expire(key, 5)
                gl.get_v("serverlogger").logger.info("加锁成功%s" % key)
                return True
            time.sleep(random.randint(1, 5) / 1000.0)

    def unlock(self, key):
        """
        : 解锁
        :param key:
        :return:
        """
        gl.get_v("serverlogger").logger.info("解锁%s" % key)
        self.__redis.delete(key)

    def setobj(self, key, obj):
        """
        : 存入对象
        :param key:
        :param obj:
        :return:
        """
        self.__redis.set(key, cPickle.dumps(obj, -1))

    def set(self, key, obj):
        """
        : 存入数组
        :param key:
        :param obj:
        :return:
        """
        self.__redis.set(key, json.dumps(obj))

    def getobj(self, key):
        """
        : 取出对象
        :param key:
        :param obj:
        :return:
        """
        jsons = self.__redis.get(key)
        obj = cPickle.loads(jsons)
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

    def publish(self, chan, msg):
        self.__redis.publish(chan, msg)
        return True

    def subscribe(self, chan):
        pub = self.__redis.pubsub()
        pub.subscribe(chan)
        pub.parse_response()
        return pub

    def sigleSubscribe(self, subject, handle):
        redis_sub = self.subscribe(subject)
        while True:
            msg = redis_sub.parse_response()
            handle(msg[2])

    def startSubscribe(self, subject, handle):
        for i in range(0, len(subject)):
            threading.Thread(target=self.sigleSubscribe, args=(subject[i], handle[i],), name=subject[i]).start()

    def _ping(self):
        while True:
            time.sleep(60)
            # 尝试向redis-server发一条消息
            if not self.__redis.ping():
                print("oops~ redis-server get lost. call him back now!")
                del self.__pool
                del self.__redis
                self.__pool = redis.ConnectionPool(host=config.get("redis", "host"),
                                                   port=int(config.get("redis", "port")),
                                                   db=0)
                self.__redis = redis.Redis(connection_pool=self.__pool)
