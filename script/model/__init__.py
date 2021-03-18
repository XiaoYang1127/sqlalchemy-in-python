#!/usr/bin/env/python
# _*_coding:utf-8_*_

from sqlalchemy_utils import database_exists, create_database, drop_database

from db.orm_db import mysql_engine, CSession
from model.base import Base, CTimestampMixin
from model.class_model import CClassModel
from model.user_model import CUserModel
from model.one_to_many import COTMCompany, COTMPhone
from model.one_to_one import COTOCompany, COTOPhone
from model.many_to_many import CMTMCompany, CMTMPhone


def init_model():
    if not database_exists(mysql_engine().url):
        create_database(mysql_engine().url)

    CClassModel.create_table(mysql_engine())
    CUserModel.create_table(mysql_engine())

    # on_to_many
    COTMCompany.create_table(mysql_engine())
    COTMPhone.create_table(mysql_engine())

    # one_to_one
    COTOCompany.create_table(mysql_engine())
    COTOPhone.create_table(mysql_engine())

    # many_to_many
    CMTMCompany.create_table(mysql_engine())
    CMTMPhone.create_table(mysql_engine())
