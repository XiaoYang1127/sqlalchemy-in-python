#!/usr/bin/env/python
# _*_coding:utf-8_*_

import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def db_url():
    host = "127.0.0.1"
    port = 3306
    user = "root"
    passwd = "mxworld2006999"
    charset = "utf8mb4"
    dbname = "orm_test"
    return "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (
        user, passwd, host, port, dbname, charset)


def mysql_engine():
    global engine
    return engine


class CSession():

    def __init__(self):
        self.session = None

    def __enter__(self):
        global session_factory
        self.session = session_factory()
        return self.session

    def __exit__(self, type, value, traceback):
        if self.session:
            self.session.close()
            self.session = None


# 初始化
if "g_orm_db" not in globals():
    g_orm_db = 1
    engine = create_engine(
        db_url(), pool_size=100, max_overflow=100,
        pool_recycle=3600, pool_timeout=3, echo=False,
        pool_pre_ping=True
    )
    session_factory = scoped_session(sessionmaker(bind=engine))
