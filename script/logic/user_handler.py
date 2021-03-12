#!/usr/local/env python
# _*_ coding:utf-8 _*_

import time

from sqlalchemy.sql import(
    select, delete, insert, update,
    and_, or_, not_, between,
    desc, asc,
    func, label,
    exists, distinct, literal, join, text
)
from sqlalchemy.dialects.mysql import insert as insert2
from tornado.log import access_log

from logic.base import CBase
from model.dbsession import CSession
from model.user_model import CUserModel
from model.class_model import CClassModel


class CUserHandler(CBase):

    def get_query_result(self, result_proxy):
        return [{column: value for column, value in row_proxy.items()} for row_proxy in result_proxy]

    def do_get(self, *args, **kwargs):
        method = self.m_query_params.get("method", "")
        func = getattr(self, method, None)
        try:
            func()
        except Exception as e:
            access_log.exception("do_get failed:%s" % str(e))
            self.simple_response(404)

    def get_user_by_id(self):
        user_id = self.m_query_params.get("user_id", None)

        # for orm query
        with CSession() as session:
            user = session.query(CUserModel).filter(
                CUserModel.id == user_id).first()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": user.to_dict() if user else {},
                    "method": "get_user_by_id",
                },
            }
            self.response_to_web(response_data)

    def query_user_by_id(self):
        user_id = self.m_query_params.get("user_id", None)
        tele = self.m_query_params.get("tele", None)

        # for sql expression query
        with CSession() as session:
            # 1. simple query
            def simple_query():
                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name.label("user_name")
                ]).where(
                    and_(CUserModel.id == user_id, CUserModel.tele == tele))
                return sql_exp

            # 2. complex query (==, >=, !=, <=, >, <) (offset, limit) (order_by, desc, asc)
            def complex_query():
                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(
                    CUserModel.tele >= tele
                ).offset(2).limit(3).order_by(
                    desc(CUserModel.updated_at), CUserModel.id
                )

            # 3. complex query2
            # (and, or_, not_, like, notlike, in_, notin_)
            def complex_query2():
                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(or_(
                    CUserModel.id == 9,
                    CUserModel.name.like("x%"),
                    not_(CUserModel.updated_at == 0)
                ))

                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(or_(
                    CUserModel.id == 9,
                    CUserModel.name.notlike("x%"),
                    CUserModel.updated_at == 0
                ))

                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(and_(
                    CUserModel.id.in_([1, 2, 3]),
                    CUserModel.age.notin_([27, ])
                ))

                return sql_exp

            # 4. group by, having
            def group_by():
                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(
                    CUserModel.tele == tele
                ).group_by(
                    CUserModel.id
                ).having(
                    func.sum(CUserModel.age) > 10
                )

                sql_exp = select([
                    CUserModel.name,
                    func.count("*").label("user_count")
                ]).where(CUserModel.tele == tele).group_by(CUserModel.name)

                sql_exp = select([
                    CUserModel.id,
                    func.sum(CUserModel.age).label("user_age_num")
                ]).where(CUserModel.tele == tele).group_by(CUserModel.id)

                return sql_exp

            # 5. distinct (id)
            def distinct():
                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(CUserModel.tele == tele).distinct()

                sql_exp = select([
                    distinct(CUserModel.id),
                    CUserModel.name
                ]).where(CUserModel.tele == tele)

                return sql_exp

            # 6. count, max, min, now相关的时间, random (select 1, select ifnull)
            def func():
                sql_exp = select([func.count(CUserModel.id)])

                sql_exp = select([func.max(CUserModel.id)])

                sql_exp = select([func.min(CUserModel.id)])

                sql_exp = select([1]).where(CUserModel.tele == tele)

                sql_exp = select([CUserModel]).where(CUserModel.tele == tele)

                sql_exp = select([
                    CUserModel.id,
                    func.ifnull(CUserModel.created_at, 100)
                ]).where(CUserModel.tele == tele)

                return sql_exp

            # 7. select exists
            def select_exists():
                exists_sql = select([1]).where(
                    CClassModel.id == CUserModel.class_id
                )
                sql_exp = select([
                    CUserModel.id,
                    CUserModel.name
                ]).where(exists(exists_sql))

                return sql_exp

            # 8. join, outerjoin
            def inner_join():
                join_sql = join(
                    CUserModel,
                    CClassModel,
                    CUserModel.class_id == CClassModel.id
                )
                sql_exp = select([
                    CClassModel.name,
                    CUserModel.name
                ]).select_from(join_sql)

                return sql_exp

            def left_join():
                join_sql = join(
                    CUserModel,
                    CClassModel,
                    CUserModel.class_id == CClassModel.id,
                    isouter=True
                )
                sql_exp = select([
                    CClassModel.name,
                    CUserModel.name
                ]).select_from(join_sql)

                return sql_exp

            def right_join():
                join_sql = join(
                    CClassModel,
                    CUserModel,
                    CClassModel.id == CUserModel.class_id,
                    isouter=True
                )
                sql_exp = select([
                    CClassModel.name,
                    CUserModel.name
                ]).select_from(join_sql)

                return sql_exp

            sql_exp = simple_query()
            result_proxy = session.execute(sql_exp)

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": self.get_query_result(result_proxy),
                    "method": "query_user_by_id",
                },
            }
            self.response_to_web(response_data)

    def do_post(self, *args, **kwargs):
        method = self.m_query_params.get("method", "")
        func = getattr(self, method, None)
        try:
            func()
        except Exception as e:
            access_log.exception("do_post failed:%s" % str(e))
            self.simple_response(404)

    def add_class(self):
        # for orm add
        with CSession() as session:
            _class = CClassModel(
                name=self.m_query_params.get("name", "ruanjian"),
                created_at=int(time.time()),
                updated_at=int(time.time()),
            )
            session.add(_class)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": _class.serialize_simple()
                },
            }
            self.response_to_web(response_data)

    def add_class_by_sql_exp(self):
        name = self.m_query_params.get("name", "ruanjian")
        created_at = int(time.time())
        updated_at = int(time.time())

        with CSession() as session:
            exists_sql = select([1]).where(CClassModel.name == name)
            select_sql = select([
                literal(name),
                literal(created_at),
                literal(updated_at)
            ]).where(~exists(exists_sql))

            sql_exp = insert(CClassModel).from_select([
                CClassModel.name,
                CClassModel.created_at,
                CClassModel.updated_at
            ], select_sql)

            result_proxy = session.execute(sql_exp)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "last_row_id": result_proxy.lastrowid,
                    "inserted_primary_key": result_proxy.inserted_primary_key,
                    "method": "add_class_by_sql_exp"
                },
            }
            self.response_to_web(response_data)

    def add_user(self):
        # for orm add
        with CSession() as session:
            user = CUserModel(
                class_id=self.m_query_params.get("class_id", 1),
                name=self.m_query_params.get("name", "xiaoming"),
                age=self.m_query_params.get("age", 0),
                addr=self.m_query_params.get("addr", "wuchang"),
                tele=self.m_query_params.get("tele", "13012345678"),
            )
            session.add(user)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": user.serialize_simple(),
                    "method": "add_user"
                },
            }
            self.response_to_web(response_data)

    def add_user_by_sql_exp(self):
        class_id = self.m_query_params.get("class_id", 1),
        name = self.m_query_params.get("name", "xiaocao")
        age = self.m_query_params.get("age", 31)
        addr = self.m_query_params.get("addr", "hankou")
        tele = self.m_query_params.get("tele", "4566")

        # for sql expression add
        with CSession() as session:
            # 1. simple insert
            def simple_insert():
                sql_exp = insert(CUserModel).values(
                    class_id=class_id,
                    name=name,
                    age=age,
                    addr=addr,
                    tele=tele,
                )

            # # 2. insert from_select
            # def insert_from_select():
            #     select_sql = select([
            #         literal(class_id),
            #         literal(name),
            #         literal(age),
            #         literal(addr),
            #         literal(tele)
            #     ]).where(CUserModel.name == "xiaocao")

            #     sql_exp = insert(CUserModel).from_select([
            #         CUserModel.class_id,
            #         CUserModel.name,
            #         CUserModel.age,
            #         CUserModel.addr,
            #         CUserModel.tele
            #     ], select_sql)

            #     return sql_exp

            # 3. insert not exists
            def insert_exists():
                exists_sql = select([1]).where(CUserModel.name == name)
                select_sql = select([
                    literal(class_id),
                    literal(name),
                    literal(age),
                    literal(addr),
                    literal(tele)
                ]).where(~exists(exists_sql))

                sql_exp = insert(CUserModel).from_select([
                    CUserModel.class_id,
                    CUserModel.name,
                    CUserModel.age,
                    CUserModel.addr,
                    CUserModel.tele], select_sql)

                return sql_exp

            # # 4. on duplicate key
            # def on_duplicate_key():
            #     insert_for_update = "name='%s',age=%d,addr='%s',updated_at=%s" % (
            #         name, age, addr, int(time.time()))
            #     sql_exp = insert(
            #         CUserModel,
            #         insert_for_update=insert_for_update
            #     ).values(
            #         class_id=class_id,
            #         name=name,
            #         age=age,
            #         addr=addr,
            #         tele=tele,
            #         created_at=int(time.time()),
            #         updated_at=int(time.time()),
            #     )

            #     return sql_exp

            # 5. on duplicate key
            def on_duplicate_key2():
                sql_exp = insert2(CUserModel).values(
                    class_id=class_id,
                    name=name,
                    age=age,
                    addr=addr,
                    tele=tele,
                    created_at=int(time.time()),
                    updated_at=int(time.time()),
                ).on_duplicate_key_update(
                    name=name,
                    age=age,
                    addr=addr,
                    updated_at=int(time.time()),
                )

                return sql_exp

            sql_exp = on_duplicate_key2()
            result_proxy = session.execute(sql_exp)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "last_row_id": result_proxy.lastrowid,
                    "inserted_primary_key": result_proxy.inserted_primary_key,
                    "method": "add_user_by_sql_exp"
                },
            }
            self.response_to_web(response_data)

    def update_user_by_id(self):
        user_id = self.m_query_params.get("user_id", 0)

        # for orm update
        with CSession() as session:
            user = session.query(CUserModel).filter(
                CUserModel.id == user_id
            ).first()

            b_update = self.update_model(user, self.m_query_params)
            if b_update:
                session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": user.serialize_detail(),
                    "method": "update_user_by_id",
                },
            }
            self.response_to_web(response_data)

    def batch_update_user_by_id(self):
        user_ids = self.m_query_params.get("user_ids", [])

        update_dict = {}
        for k, v in self.m_query_params.items():
            if not hasattr(CUserModel, k):
                continue
            update_dict[k] = v

        # for orm update
        with CSession() as session:
            user = session.query(CUserModel).filter(
                CUserModel.id.in_(user_ids)
            ).update(update_dict, synchronize_session=False)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": user.serialize_detail(),
                    "method": "batch_update_user_by_id",
                },
            }
            self.response_to_web(response_data)

    def delete_user_by_id(self):
        user_ids = self.m_query_params.get("user_ids", [])

        with CSession() as session:
            users = session.query(CUserModel).filter(
                CUserModel.id.in_(user_ids)
            ).delete(synchronize_session=False)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {},
            }
            self.response_to_web(response_data)
