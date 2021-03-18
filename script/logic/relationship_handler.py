
import datetime

from sqlalchemy.sql import func
from tornado.log import access_log

from logic.base import CBase
from model import (
    CSession,
    COTMCompany,
    COTMPhone,
    COTOCompany,
    COTOPhone,
    CMTMCompany,
    CMTMPhone
)

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


class CRelationshipHandler(CBase):

    def do_get(self, *args, **kwargs):
        method = self.m_query_params.get("method", "")
        get_func = getattr(self, method, None)
        try:
            get_func()
        except Exception as e:
            access_log.exception("do_get failed:%s" % str(e))
            self.simple_response(404)

    def do_post(self, *args, **kwargs):
        method = self.m_query_params.get("method", "")
        post_func = getattr(self, method, None)
        try:
            post_func()
        except Exception as e:
            access_log.exception("do_post failed:%s" % str(e))
            self.simple_response(404)

    def add_one_to_many(self):
        # add company
        with CSession() as session:
            for n, l in companys.items():
                new_company = COTMCompany(
                    name=n,
                    location=l
                )
                session.add(new_company)
            session.commit()

        # add phone
        with CSession() as session:
            for name, company_id, price in phones:
                new_phone = COTMPhone(
                    name=name,
                    price=price,
                    company_id=company_id,
                )
                session.add(new_phone)
            session.commit()

        # for response
        response_data = {
            "method": "add_one_to_many"
        }
        self.response_to_web(response_data)

    def query_one_to_many(self):
        phone_id = self.m_query_params.get("phone_id", None)
        company_id = self.m_query_params.get("company_id", None)
        data = {}

        if phone_id:
            with CSession() as session:
                phone = session.query(COTMPhone).filter_by(
                    id=phone_id
                ).first()

                # 反向查询
                data = {
                    "c_name": phone.rs_company.name
                }
                data.update(phone.save())
        elif company_id:
            with CSession() as session:
                company = session.query(COTMCompany).filter_by(
                    id=company_id
                ).first()

                # 正向查询
                data = {
                    "p_name": [obj.name for obj in company.rs_phone]
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
                "method": "query_one_to_many",
            },
        }
        self.response_to_web(response_data)

    def add_one_to_one(self):
        # add company
        with CSession() as session:
            for n, l in companys.items():
                new_company = COTOCompany(
                    name=n,
                    location=l
                )
                session.add(new_company)
            session.commit()

        # add phone
        with CSession() as session:
            for name, company_id, price in phones:
                new_phone = COTOPhone(
                    name=name,
                    price=price,
                    company_id=company_id
                )
                session.add(new_phone)
            session.commit()

        # for response
        response_data = {
            "method": "add_one_to_one"
        }
        self.response_to_web(response_data)

    def query_one_to_one(self):
        phone_id = self.m_query_params.get("phone_id", None)
        company_id = self.m_query_params.get("company_id", None)
        data = {}

        if phone_id:
            with CSession() as session:
                phone = session.query(COTOPhone).filter_by(
                    id=phone_id
                ).first()

                data = {
                    "c_name": phone.rs_company.name
                }
                data.update(phone.save())
        elif company_id:
            with CSession() as session:
                company = session.query(COTOCompany).filter_by(
                    id=company_id
                ).first()

                data = {
                    "p_name": [obj.name for obj in company.rs_phone]
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
                "method": "query_one_to_one",
            },
        }
        self.response_to_web(response_data)

    def add_many_to_many(self):
        # add company
        with CSession() as session:
            for n, l in companys.items():
                new_company = CMTMCompany(
                    name=n,
                    location=l
                )
                session.add(new_company)
            session.commit()

        # add phone
        with CSession() as session:
            for name, _, price in phones:
                new_phone = CMTMPhone(
                    name=name,
                    price=price,
                )
                session.add(new_phone)
            session.commit()

        # for response
        response_data = {
            "method": "add_many_to_many"
        }
        self.response_to_web(response_data)

    def query_many_to_many(self):
        phone_id = self.m_query_params.get("phone_id", None)
        company_id = self.m_query_params.get("company_id", None)
        data = {}

        if phone_id:
            with CSession() as session:
                phone = session.query(CMTMPhone).filter_by(
                    id=phone_id
                ).first()

                data = {
                    "c_name": phone.rs_company.name
                }
                data.update(phone.save())
        elif company_id:
            with CSession() as session:
                company = session.query(CMTMCompany).filter_by(
                    id=company_id
                ).first()

                data = {
                    "p_name": [obj.name for obj in company.rs_phone]
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
                "method": "query_many_to_many",
            },
        }
        self.response_to_web(response_data)
