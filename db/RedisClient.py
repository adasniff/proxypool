# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 27/04/2017

import json
import redis
from util.ClassUtils import Singleton


class RedisClient(metaclass=Singleton):
    """
    redis client
    """

    def __init__(self, host, port, db, password, max_conns=50):
        pool = redis.ConnectionPool(max_connections=max_conns, host=host, port=port, db=db, password=password)
        self._conn = redis.Redis(connection_pool=pool)

    def lpushlist(self, name, values=[]):
        if isinstance(values, list):
            for value in values:
                self.lpush(name, value)

    def lpush(self, name, value):
        value = json.dumps(value) if isinstance(value, dict) else value
        return self._conn.lpush(name, value)

    def brpop(self, name, timeout=10):
        return self._conn.brpop(name, timeout=timeout)

    def llen(self, name):
        return self._conn.llen(name)

    def set(self, name, value, ex, nx=True):
        return self._conn.set(name, value, ex, nx=nx)

    def get(self, name):
        return self._conn.get(name)

    def delete(self, name):
        return self._conn.delete(name)

    def incr(self, name, amount=1):
        return self._conn.incr(name, amount)

    def decr(self, name, amount=1):
        return self._conn.decr(name, amount)

    def exist(self, name):
        return self._conn.exists(name)

    def sadd(self, name, *values):
        return self._conn.sadd(name, *values)

    def srem(self, name, value):
        return self._conn.srem(name, value)

    def srandmember(self, name):
        return self._conn.srandmember(name)

    def scard(self, name):
        return self._conn.scard(name)

    def spop(self, name):
        return self._conn.spop(name)

    def hset(self, name, key, value):
        return self._conn.hset(name, key, value)

    def hget(self, name, key):
        return self._conn.hget(name, key)

    def hincrby(self, name, key, amount):
        return self._conn.hincrby(name, key, amount)

    def hdel(self, name, key):
        return self._conn.hdel(name, key)
