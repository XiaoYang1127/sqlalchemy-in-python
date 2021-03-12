#!/usr/bin/env/python
# _*_coding:utf-8_*_

import os
import threading
import traceback

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.log import access_log

import httpserver.application


class CHttpServer(threading.Thread):

    def __init__(self, http_port):
        threading.Thread.__init__(self)
        self.m_http_port = http_port
        self.m_http_server = None

    def make_app(self):
        return tornado.web.Application(
            httpserver.application.HANDLERS,
            log_function=self.LogRequest,
            autoreload=True,
        )

    def run(self):
        try:
            access_log.info("HTTP_SERVER started，http_port:%d" %
                            self.m_http_port)
            self.m_http_server = tornado.httpserver.HTTPServer(
                self.make_app(), xheaders=True)
            self.m_http_server.listen(self.m_http_port)
            tornado.ioloop.IOLoop.instance().start()
        except Exception:
            try:
                traceback.print_exc()
            except Exception:
                pass

            pid = os.getpid()
            os.kill(pid, 15)

    def LogRequest(self, handler):
        request_time = 1000.0 * handler.request.request_time()
        access_log.info("%d %s %.2fms" %
                        (handler.get_status(),
                         handler.request_summary(),
                         request_time))


# 初始化
if "g_http_server" not in globals():
    g_http_server = None


def init_http_server(http_port=5088):
    global g_http_server
    if g_http_server:
        return

    g_http_server = CHttpServer(http_port)
    g_http_server.start()
