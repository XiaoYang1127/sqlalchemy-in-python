#!/usr/bin/env/python
# _*_coding:utf-8_*_

import time

import sqlalchemy.exc

from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class CDBSession(object):

    def __init__(self):
        self.m_engine = self.create_engine()
        self.m_factory = self.session_maker()
        self.m_session = None
        self.init_session()

    def init_session(self):
        self.m_session = self.m_factory()

    def get_config(self):
        host = "127.0.0.1"
        port = 3306
        user = "root"
        passwd = "your password"
        charset = "utf8mb4"
        dbname = "orm_test"
        return "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (user, passwd, host, port, dbname, charset)

    def create_engine(self):
        """
        pool_size      #连接池大小
        max_overflow   #超过连接池后，允许最大扩展的连接数
        pool_timeout   #连接池最大等待时间设置
        pool_recycle   #连接回收时间, 如果设置为-1，表示没有no timeout, 注意，mysql会自动断开超过8小时的连接
        echo           #启用它后，我们将看到生成的所有SQL
        :return:
        """
        return create_engine(
            self.get_config(), pool_size=100, max_overflow=100,
            pool_recycle=3600, pool_timeout=3, echo=False,
            pool_pre_ping=True
        )

    def session_maker(self):
        return scoped_session(sessionmaker(bind=self.m_engine))

    def get_engine(self):
        return self.m_engine

    def get_session(self):
        return self.m_session

    def add(self, instance, _warn=True):
        """增加单个模型"""
        self.get_session().add(instance, _warn)

    def add_all(self, instances):
        """增加多个模型"""
        self.get_session().add_all(instances)

    def query(self, *entities, **kwargs):
        return self.get_session().query(*entities, **kwargs)

    def delete(self, instance):
        return self.get_session().delete(instance)

    def delete_all(self, instances):
        for instance in instances:
            self.delete(instance)

    def execute(self, clause, params=None, mapper=None, bind=None, **kw):
        try:
            return self.get_session().execute(clause, params=params, mapper=mapper, bind=bind, **kw)
        except (sqlalchemy.exc.OperationalError,):
            print("%s execute failed for mysql has gone away" % (self.__class__.__name__))
            if self.m_session:
                self.m_session.rollback()
                self.m_session = None
                self.m_factory = self.session_maker()

    def commit(self):
        try:
            self.get_session().commit()
            return 1
        except Exception as e:
            print("%s commit failed:%s" % (self.__class__.__name__, str(e)))
            self.get_session().rollback()
            return 0


if not "g_dbSession" in globals():
    g_dbSession = None


def Instance():
    global g_dbSession
    if not g_dbSession:
        g_dbSession = CDBSession()
    return g_dbSession
