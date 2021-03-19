#!/usr/bin/env/python
# _*_coding:utf-8_*_
"""
sqlalchemy version must greater 1.4.0
"""

import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


def db_url():
    host = "127.0.0.1"
    port = 3306
    user = "root"
    passwd = "mxworld2006999"
    charset = "utf8mb4"
    dbname = "orm_test"
    return "mysql+aiomysql://%s:%s@%s:%s/%s?charset=%s" % (
        user, passwd, host, port, dbname, charset)


async_engine = create_async_engine(
    db_url(), pool_size=100, max_overflow=100,
    pool_recycle=3600, pool_timeout=3, echo=False,
    pool_pre_ping=True
)

async_session = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)
