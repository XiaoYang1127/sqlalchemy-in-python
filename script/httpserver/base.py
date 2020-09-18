#!/usr/bin/env/python
# _*_coding:utf-8_*_

import json
import time
import functools

import tornado.gen
import tornado.ioloop


class CBaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.m_query_params = {}
        self.__timeout = self.ioloop().add_timeout(int(time.time()) + 30, functools.partial(self.simple_response, 408))

    def is_valid_request(self):
        return 1

    def headers(self):
        return self.request.headers

    def get_headers(self, key, default=None):
        return self.headers().get(key, default)

    def get_query_params(self):
        return self.m_query_params

    def ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    @tornado.web.asynchronous
    def head(self, *args, **kwargs):
        self.do_head(*args, **kwargs)

    def do_head(self, *args, **kwargs):
        self.simple_response(405)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.do_get(*args, **kwargs)

    def do_get(self, *args, **kwargs):
        self.simple_response(405)

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self.do_post(*args, **kwargs)

    def do_post(self, *args, **kwargs):
        self.simple_response(405)

    @tornado.web.asynchronous
    def delete(self, *args, **kwargs):
        self.do_delete(*args, **kwargs)

    def do_delete(self, *args, **kwargs):
        self.simple_response(405)

    @tornado.web.asynchronous
    def patch(self, *args, **kwargs):
        self.do_patch(*args, **kwargs)

    def do_patch(self, *args, **kwargs):
        self.simple_response(405)

    @tornado.web.asynchronous
    def put(self, *args, **kwargs):
        self.do_put(*args, **kwargs)

    def do_put(self, *args, **kwargs):
        self.simple_response(405)

    @tornado.web.asynchronous
    def options(self, *args, **kwargs):
        self.do_options(*args, **kwargs)

    def do_options(self, *args, **kwargs):
        self.simple_response(405)

    def simple_response(self, result, desc=""):
        res_dict = {}
        res_dict["status_code"] = result
        res_dict["message"] = desc
        self.ioloop().add_callback(self._response, res_dict)

    def response_to_web(self, res_dict=None):
        self.ioloop().add_callback(self._response, res_dict)

    def _response(self, chunk=None):
        if self._finished:
            return

        chunk = chunk or {}
        if isinstance(chunk, dict):
            self.set_header("Content-Type", "application/json; charset=utf-8")
            chunk = json.dumps(chunk, ensure_ascii=False)

        self.write(chunk)
        self.finish()

    def on_finish(self):
        self.ioloop().remove_timeout(self.__timeout)
