from tornado.log import access_log

from logic.base import CBase
from model import CSession


class CParserSqlHandler(CBase):

    def get_query_result(self, result_proxy):
        return [{column: str(value) for column, value in row_proxy.items()} for row_proxy in result_proxy]

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

    def query_by_safe(self):
        id = self.m_query_params.get("id", "")

        with CSession() as session:
            sql = "select * from test_user where id=:id"
            result_proxy = session.execute(sql, {"id": id})
            self.response_to_web({
                "code": 200,
                "data": self.get_query_result(result_proxy)
            })

    def query_by_unsafe(self):
        id = self.m_query_params.get("id", "")

        with CSession() as session:
            sql = "select * from test_user where id=%s" % id
            result_proxy = session.execute(sql)
            data = self.get_query_result(result_proxy) or []
            self.response_to_web({
                "id": id,
                "code": 200,
                "data": len(data)
            })
