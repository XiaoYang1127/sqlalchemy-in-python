"""
note:
    1. Insert, Update, Delete by sql expression cant't be to listen by events
    2. the differences between in "update" and "update exists"
    3. delete exists, delete where, delete join(left, right, inner)
"""

import time

from sqlalchemy import Column, Integer, event
from sqlalchemy.sql.expression import Insert, Update, Delete, Select
from sqlalchemy.ext.compiler import compiles

import db.redis_db


class CBase(object):

    __table__ = None
    ex_time = 24 * 60 * 60
    no_save_redis = 0
    skip_created_at = 0
    skip_updated_at = 0

    created_at = Column(Integer, default=0)
    updated_at = Column(Integer, default=0)

    def save(self):
        raise NotImplementedError("save undefined")

    def load(self, data):
        raise NotImplementedError("load undefined")

    def save_to_redis(self):
        to_save = self.save()
        redis_client = db.redis_db.GetRedisConn()
        redis_client.myset("%s:%s" % (self.__table__, self.id), to_save, ex=self.ex_time, serialize=True)

    def load_from_redis(self, unique_id):
        redis_client = db.redis_db.GetRedisConn()
        from_load = redis_client.myget("%s:%s" % (self.__table__, unique_id), {}, serialize=True)
        self.load(from_load)

    def delete_from_redis(self):
        redis_client = db.redis_db.GetRedisConn()
        redis_client.delete("%s:%s" % (self.__table__, self.id))

    def tbl_cols(self):
        return self.__table__.columns

    def to_dict(self):
        return {col.name: getattr(self, col.name, None) for col in self.tbl_cols()}


@event.listens_for(CBase, 'before_update', propagate=True)
def before_update(mapper, connection, target):
    if target.skip_updated_at:
        return
    target.updated_at = int(time.time())


@event.listens_for(CBase, 'after_update', propagate=True)
def after_update(mapper, connection, target):
    if target.no_save_redis:
        return
    target.save_to_redis()


@event.listens_for(CBase, 'before_insert', propagate=True)
def before_insert(mapper, connection, target):
    if target.skip_created_at:
        return
    target.created_at = int(time.time())
    target.updated_at = int(time.time())


@event.listens_for(CBase, 'after_insert', propagate=True)
def after_insert(mapper, connection, target):
    if target.no_save_redis:
        return
    target.save_to_redis()


@event.listens_for(CBase, 'after_delete', propagate=True)
def after_delete(mapper, connection, target):
    if target.no_save_redis:
        return
    target.delete_from_redis()


@compiles(Insert)
def insert_for_update(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'insert_for_update' in insert.kwargs:
        return s + " ON DUPLICATE KEY UPDATE " + insert.kwargs['insert_for_update']
    return s
