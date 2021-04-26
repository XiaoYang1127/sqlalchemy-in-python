from tornado.log import access_log

from logic.base import CBase
from model import CSession, CUserModel


class COrmHandler(CBase):

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

    def test_autoflush(self):
        with CSession() as session:
            user = CUserModel(
                class_id=self.m_query_params.get("class_id", 1),
                name=self.m_query_params.get("name", "xiaoming11"),
                age=self.m_query_params.get("age", 0),
                addr=self.m_query_params.get("addr", "wuchang"),
                tele=self.m_query_params.get("tele", "130123456777"),
            )
            session.add(user)

            user = session.query(CUserModel).filter(
                CUserModel.name == "xiaoming11"
            ).first()

            # 设置autoflush=True，能查询到结果；否则查询的是none
            # session.commit()

            # for response
            response_data = {
                "status_code": 200,
                "message": "success",
                "payload": {
                    "data": user.serialize_detail(),
                    "method": "test_autoflush",
                },
            }
            self.response_to_web(response_data)
