#!/usr/bin/env/python
# _*_coding:utf-8_*_

from sqlalchemy_utils import database_exists, create_database, drop_database

from db.orm_db import mysql_engine, CSession
from model.base import Base, CTimestampMixin
from model.class_model import CClassModel
from model.user_model import CUserModel
from model.relation_model import CUser, CRole


def init_model():
    if not database_exists(mysql_engine().url):
        create_database(mysql_engine().url)

    CClassModel.create_table(mysql_engine())
    CUserModel.create_table(mysql_engine())
    CUser.create_table(mysql_engine())
    CRole.create_table(mysql_engine())
