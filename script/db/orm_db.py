#!/usr/bin/env/python
# _*_coding:utf-8_*_

import time

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            try:
                if exc_val is None:
                    self.session.commit()
                elif isinstance(exc_val, SQLAlchemyError):
                    self.session.rollback()
            except SQLAlchemyError:
                self.session.rollback()
            finally:
                self.session.close()
                self.session = None


# 初始化
if "session_factory" not in globals():
    engine = create_engine(
        db_url(), pool_size=100, max_overflow=100,
        pool_recycle=3600, pool_timeout=3, echo=True,
        pool_pre_ping=False
    )

    # flush：将当前 session 存在的变更发送给数据库，即让数据库执行 SQL 语句
    # commit, 提交一个事务。一个事务可能有一条 SQL 或者多条 SQL 语句
    # autoflush=True，session 进行查询之前会自动吧当前累计的修改发送到数据库，即自动执行一次 flush 的操作
    # autocommit=True, 需要显式调用 session.begin() 方法来开启事务；否则 session 在实例化之后即处于begin状态
    # expire_on_commit=True，commit 之后所有实例都会过期，之后再访问这些过期实例的属性时，SQLAlchemy 会重新去数据库加载实例对应的数据记录
    session_factory = scoped_session(sessionmaker(
        bind=engine,
        autoflush=True,
        autocommit=False,
        expire_on_commit=False,
    ))
