#!/usr/local/env python
# _*_ coding:utf-8 _*_

import datetime

from sqlalchemy.sql import(
    select, delete, insert, update,
    and_, or_, not_, between,
    desc, asc,
    func, label,
    exists, distinct, literal, join, text
)
from sqlalchemy.dialects.mysql import insert as dialects_insert
from tornado.log import access_log

from logic.base import CBase
from model import CSession, CClassModel, CUserModel, CCompany, CPhone


class CUserHandler(CBase):

    def get_query_result(self, result_proxy):
        return [{column: value for column, value in row_proxy.items()} for row_proxy in result_proxy]

    def do_get(self, *args, **kwargs):
        method = self.m_query_params.get("method", "")
        get_func = getattr(self, method, None)
        try:
            get_func()
        except Exception as e:
            access_log.exception("do_get failed:%s" % str(e))
            self.simple_response(404)

    def add_relationship(self):
        companys = {
            "Apple": "Amercian",
            "Xiaomi": "China",
            "Huawei": "China",
            "Sungsum": "Korea",
            "Nokia": "Finland"
        }
        phones = (
            ["iphoneX", 1, 8400],
            ["xiaomi2s", 2, 3299],
            ["Huaweimate10", 3, 3399],
            ["SungsumS8", 4, 4099],
            ["NokiaLumia", 5, 2399],
            ["iphone4s", 1, 3800]
        )

        # add company
        with CSession() as session:
            for n, l in companys.items():
                new_company = CCompany(
                    name=n,
                    location=l
                )
                session.add(new_company)
            session.commit()

        # add phone
        with CSession() as session:
            for name, company_id, price in phones:
                new_phone = CPhone(
                    name=name,
                    price=price,
                    company_id=company_id,
                )
                session.add(new_phone)
            session.commit()

        # for response
        response_data = {
            "method": "add_relationship"
        }
        self.response_to_web(response_data)

    def query_relationship(self):
        """
        1. company是主表，phone是从表。查询phone表，返回phone_obj，可以通过phone_obj.Company查询到company中外键关联的数据。
        查phone表返回company表里的数据。这个称之为：正向查询。

        2. company是主表，phone是从表。查询company表，返回company_obj，可以通过company_obj.phone_of_company查询到phone表的外键关联数据。
        查company表返回phone表里的数据。这个称之为：反向查询
        """
        phone_id = self.m_query_params.get("phone_id", None)
        company_id = self.m_query_params.get("company_id", None)
        data = {}

        if phone_id:
            with CSession() as session:
                phone = session.query(CPhone).filter(
                    CPhone.id == phone_id
                ).first()

                data = {
                    "c_name": phone.company.name
                }
                data.update(phone.save())
        elif company_id:
            with CSession() as session:
                company = session.query(CCompany).filter(
                    CCompany.id == company_id
                ).first()

                data = {
                    "p_name": [obj.name for obj in company.phone_of_company]
                }
                data.update(company.save())
        else:
            data = {}

        # for response
        response_data = {
            "status_code": 200,
            "message": "success",
            "payload": {
                "data": data,
                "method": "query_user_by_id",
            },
        }
        self.response_to_web(response_data)

    def check_user_exists(self):
        user_id = self.m_query_params.get("user_id", None)

        with CSession() as session:
            is_exists = session.query(CUserModel.id).filter(
                CUserModel.id == user_id
            ).one_or_none()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "user_id": user_id,
                    "data": is_exists,
                    "method": "check_user_exists",
                },
            }
            self.response_to_web(response_data)

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
        def db_func():
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

        def do_join():
            sql_exp = session.query(CUserModel).join(
                CClassModel, CUserModel.class_id == CClassModel.id
            ).filter(
                CUserModel.id == user_id
            )

            return sql_exp

        # for sql expression query
        with CSession() as session:
            sql_exp = do_join()
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
        post_func = getattr(self, method, None)
        try:
            post_func()
        except Exception as e:
            access_log.exception("do_post failed:%s" % str(e))
            self.simple_response(404)

    def add_class(self):
        with CSession() as session:
            new_model = CClassModel(
                name=self.m_query_params.get("name", "ruanjian"),
            )
            session.add(new_model)
            session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": new_model.serialize_simple()
                },
            }
            self.response_to_web(response_data)

    def add_class_by_sql_exp(self):
        name = self.m_query_params.get("name", "ruanjian")
        now = datetime.datetime.now()

        with CSession() as session:
            exists_sql = select([1]).where(CClassModel.name == name)
            select_sql = select([
                literal(name),
                literal(now),
                literal(now)
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

    def add_user_by_sql(self):
        user_id = self.m_query_params.get("user_id", None)
        with CSession() as session:
            session.execute('select * from User')
            session.execute("insert into test_user(name, age) values('bomo', 13)")
            session.execute("insert into test_user(name, age) values(:name, :age)",
                            {'name': 'bomo', 'age': 12})

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": None,
                    "method": "add_user_by_sql"
                },
            }
            self.response_to_web(response_data)

    def add_user(self):
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
        now = datetime.datetime.now()

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
            #         name, age, addr, now)
            #     sql_exp = insert(
            #         CUserModel,
            #         insert_for_update=insert_for_update
            #     ).values(
            #         class_id=class_id,
            #         name=name,
            #         age=age,
            #         addr=addr,
            #         tele=tele,
            #         created_at=now,
            #         updated_at=now,
            #     )

            #     return sql_exp

            # 5. on duplicate key
            def on_duplicate_key2():
                sql_exp = dialects_insert(CUserModel).values(
                    class_id=class_id,
                    name=name,
                    age=age,
                    addr=addr,
                    tele=tele,
                    created_at=now,
                    updated_at=now,
                ).on_duplicate_key_update(
                    name=name,
                    age=age,
                    addr=addr,
                    updated_at=now,
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
