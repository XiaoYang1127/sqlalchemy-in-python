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

import logic.base
import model.dbsession

from model.user_model import CUserModel
from model.class_model import CClassModel


class CUserHandler(logic.base.CBase):

    def do_get(self, *args, **kwargs):
        method = self.m_query_params.get('method', '')  # for self-define method
        func = getattr(self, method, None)
        try:
            func()
        except Exception as e:
            print('do_get failed:%s' % str(e))
            self.simple_response(404)

    def get_user_by_id(self):
        user_id = self.m_query_params.get('user_id', None)

        # for orm query
        session = model.dbsession.Instance()
        user = session.query(CUserModel).filter(CUserModel.id == user_id).first()

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {
                'data': user.to_dict() if user else {}
            },
        }
        self.response_to_web(response_data)

    def query_user_by_id(self):
        user_id = self.m_query_params.get('user_id', None)
        tele = self.m_query_params.get('tele', None)

        # for sql expression query
        session = model.dbsession.Instance()

        # # 1. simple query
        # sql_exp = select([CUserModel.id, CUserModel.name.label('user_name')]).where(and_(CUserModel.id == user_id, CUserModel.tele == tele))

        # # 2. complex query (==, >=, !=, <=, >, <) (offset, limit) (order_by, desc, asc)
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(CUserModel.tele >= tele).offset(
        #     2).limit(3).order_by(desc(CUserModel.updated_at), CUserModel.id)

        # # 3. complex query2 (and, or_, not_, like, notlike, in_, notin_)
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(
        #     or_(CUserModel.id == 9, CUserModel.name.like('x%'), not_(CUserModel.updated_at == 0)))
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(
        #     or_(CUserModel.id == 9, CUserModel.name.notlike('x%'), CUserModel.updated_at == 0))
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(and_(CUserModel.id.in_([1, 2, 3]), CUserModel.age.notin_([27, ])))

        # # 4. group by, having
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(
        #     CUserModel.tele == tele).group_by(CUserModel.id).having(func.sum(CUserModel.age) > 10)
        # sql_exp = select([CUserModel.name, func.count('*').label('user_count')]).where(CUserModel.tele == tele).group_by(CUserModel.name)
        # sql_exp = select([CUserModel.id, func.sum(CUserModel.age).label('user_age_num')]
        #                  ).where(CUserModel.tele == tele).group_by(CUserModel.id)

        # # 5. distinct (id)
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(CUserModel.tele == tele).distinct()
        # sql_exp = select([distinct(CUserModel.id), CUserModel.name]).where(CUserModel.tele == tele)

        # # 6. count, max, min, now相关的时间, random (select 1, select ifnull)
        # sql_exp = select([func.count(CUserModel.id)])
        # sql_exp = select([func.max(CUserModel.id)])
        # sql_exp = select([func.min(CUserModel.id)])
        # sql_exp = select([1]).where(CUserModel.tele == tele)
        # sql_exp = select([CUserModel]).where(CUserModel.tele == tele)
        # sql_exp = select([CUserModel.id, func.ifnull(CUserModel.created_at, 100)]).where(CUserModel.tele == tele)

        # # 7. select exists
        # exists_sql = select([1]).where(CClassModel.id == CUserModel.class_id)
        # sql_exp = select([CUserModel.id, CUserModel.name]).where(exists(exists_sql))

        # # 8. join, outerjoin
        # innerjoin
        # join_sql = join(CUserModel, CClassModel, CUserModel.class_id == CClassModel.id)
        # sql_exp = select([CClassModel.name, CUserModel.name]).select_from(join_sql)
        # # leftjoin
        # join_sql = join(CUserModel, CClassModel, CUserModel.class_id == CClassModel.id, isouter=True)
        # sql_exp = select([CClassModel.name, CUserModel.name]).select_from(join_sql)
        # # rightjoin
        join_sql = join(CClassModel, CUserModel, CClassModel.id == CUserModel.class_id, isouter=True)
        sql_exp = select([CClassModel.name, CUserModel.name]).select_from(join_sql)

        result_proxy = session.execute(sql_exp)

        ret_list = result_proxy.fetchall()

        # for pack data
        ret_dict = []
        try:
            for id, name in ret_list:
                ret_dict.append({
                    'id': id,
                    'name': name,
                })
        except:
            for k, in ret_list:
                ret_dict.append({
                    "num": k,
                })

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {
                'data': ret_dict
            },
        }
        self.response_to_web(response_data)

    def do_post(self, *args, **kwargs):
        method = self.m_query_params.get('method', '')  # for self-define method
        func = getattr(self, method, None)
        try:
            func()
        except Exception as e:
            print('do_post failed:%s' % str(e))
            self.simple_response(404)

    def add_class(self):
        # for orm add
        session = model.dbsession.Instance()
        _class = CClassModel(
            name=self.m_query_params.get('name', 'ruanjian'),
        )
        session.add(_class)
        session.commit()

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {
                'data': _class.serialize_simple()
            },
        }
        self.response_to_web(response_data)

    def add_user(self):
        # for orm add
        session = model.dbsession.Instance()
        user = CUserModel(
            class_id=self.m_query_params.get('class_id', 1),
            name=self.m_query_params.get('name', 'xiaoming'),
            age=self.m_query_params.get('age', 0),
            addr=self.m_query_params.get('addr', 'wuchang'),
            tele=self.m_query_params.get('tele', '13012345678'),
        )
        session.add(user)
        session.commit()

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {
                'data': user.serialize_simple()
            },
        }
        self.response_to_web(response_data)

    def add_user_by_sql_exp(self):
        class_id = self.m_query_params.get('class_id', 1),
        name = self.m_query_params.get('name', 'xiaocao')
        age = self.m_query_params.get('age', 31)
        addr = self.m_query_params.get('addr', 'hankou')
        tele = self.m_query_params.get('tele', '4566')

        # for sql expression add
        session = model.dbsession.Instance()
        # # 1. simple insert
        # sql_exp = insert(CUserModel).values(
        #     class_id=class_id,
        #     name=name,
        #     age=age,
        #     addr=addr,
        #     tele=tele,
        # )

        # # 2. insert from_select
        # select_sql = select([literal(class_id), literal(name), literal(age), literal(addr), literal(tele)]).where(CUserModel.name == "xiaocao")
        # sql_exp = insert(CUserModel).from_select([CUserModel.class_id, CUserModel.name, CUserModel.age, CUserModel.addr, CUserModel.tele], select_sql)

        # 3. insert exists
        # exists_sql = select([1]).where(CUserModel.name == name)
        # select_sql = select([literal(class_id), literal(name), literal(age), literal(addr), literal(tele)]).where(~exists(exists_sql))
        # sql_exp = insert(CUserModel).from_select([CUserModel.class_id, CUserModel.name,
        #                                           CUserModel.age, CUserModel.addr, CUserModel.tele], select_sql)

        # 4. on duplicate key
        # insert_for_update = "name='%s',age=%d,addr='%s',updated_at=%s" % (name, age, addr, int(time.time()))
        # sql_exp = insert(CUserModel, insert_for_update=insert_for_update).values(
        #     class_id=class_id,
        #     name=name,
        #     age=age,
        #     addr=addr,
        #     tele=tele,
        #     created_at=int(time.time()),
        #     updated_at=int(time.time()),
        # )

        # 5. on duplicate key
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

        proxy_result = session.execute(sql_exp)
        session.commit()
        id = proxy_result.inserted_primary_key  # 多列插入的时候，该值为NULL

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {
                'data': id
            },
        }
        self.response_to_web(response_data)

    def update_user_by_id(self):
        user_id = self.m_query_params.get('user_id', 0)

        # for orm update
        session = model.dbsession.Instance()
        user = session.query(CUserModel).filter(CUserModel.id == user_id).first()
        b_update = self.update_model(user, self.m_query_params)
        if b_update:
            session.commit()

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {
                'data': user.serialize_detail()
            },
        }
        self.response_to_web(response_data)

    def delete_user_by_id(self):
        # for orm delete
        # user_id = self.m_query_params.get('user_id', 0)
        # session = model.dbsession.Instance()
        # query_model = session.query(CUserModel).filter(CUserModel.id == user_id)
        # query_model.delete()
        # session.commit()

        # for session delete
        user_name = self.m_query_params.get('user_name', 0)
        session = model.dbsession.Instance()
        users = session.query(CUserModel).filter(CUserModel.name == user_name)
        session.delete_all(users)
        session.commit()

        # for response
        response_data = {
            'status_code': 200,
            'message': 'success',
            'payload': {},
        }
        self.response_to_web(response_data)
