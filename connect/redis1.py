# coding=utf-8
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


def lock(lockedKey, timeout):
    t = time.time()
    nano = int(round(t * 1000000000))
    timeoutNanos = timeout * 1000000L
    while (int(round(time.time() * 1000000000)) - nano) < timeoutNanos:
        if r.setnx(lockedKey, time.strftime("%Y%m%d%H%M%S", time.localtime())) == 1:
            r.expire(lockedKey, 5)
            return True
        time.sleep(0.002)
    return False


def unlock(lockedKey):
    r.delete(lockedKey)


if __name__ == '__main__':
    lock("locksss", 2000)
    time.sleep(1)
    print(r.exists("locksss"))
    time.sleep(1)
    print(r.exists("locksss"))
    unlock("locksss")
    time.sleep(1)
    print(r.exists("locksss"))
    time.sleep(1)
    print(r.exists("locksss"))
    time.sleep(1)
    print(r.exists("locksss"))
