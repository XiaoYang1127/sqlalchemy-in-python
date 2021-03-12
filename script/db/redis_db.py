#!/usr/bin/env/python
# _*_coding:utf-8_*_

import pickle
import redis

# 初始化
if not "g_redis_conn" in globals():
    g_redis_conn = {}


def GetRedisConn(db=0):
    global g_redis_conn
    conn = g_redis_conn.get(db)
    if not conn:
        connection_pool = redis.ConnectionPool(
            max_connections=50,
            host="localhost",
            port=6379,
            socket_keepalive=True,
            db=db,
            password="mxworld2006999",
            decode_responses=True
        )
        conn = CRedisConn(db=db, connection_pool=connection_pool)
        g_redis_conn[db] = conn

    return conn


class CRedisConn(redis.Redis):

    def __init__(self, db=None, connection_pool=None):
        redis.Redis.__init__(self, db=db, connection_pool=connection_pool)

    def myset(self, key, value, ex=None, serialize=False):
        if serialize:
            value = pickle.dumps(value).decode('latin1')
        result = self.set(key, value, ex)
        return result

    def myget(self, key, default=None, serialize=False):
        result = self.get(key)
        if not result:
            return default
        if serialize:
            result = pickle.loads(result.encode('latin1'))
        return result
