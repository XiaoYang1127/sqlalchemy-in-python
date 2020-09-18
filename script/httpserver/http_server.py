#!/usr/bin/env/python
# _*_coding:utf-8_*_

import os
import threading
import traceback

import tornado.httpserver
import tornado.ioloop
import tornado.web

import httpserver.application


class CHttpServer(threading.Thread):

    def __init__(self, http_port):
        threading.Thread.__init__(self)
        self.m_http_port = http_port
        self.m_http_server = None

    def make_app(self):
        return tornado.web.Application(httpserver.application.HANDLERS, log_function=self.LogRequest)

    def run(self):
        try:
            print("HTTP_SERVER started，http_port:%d" % self.m_http_port)
            self.m_http_server = tornado.httpserver.HTTPServer(self.make_app(), xheaders=True)
            self.m_http_server.listen(self.m_http_port)
            tornado.ioloop.IOLoop.instance().start()
        except:
            try:
                traceback.print_exc()
            except:
                pass

            pid = os.getpid()
            os.kill(pid, 15)

    def LogRequest(self, handler):
        request_time = 1000.0 * handler.request.request_time()
        if request_time >= 1000:
            print("api: %s timeout %.2fms" % (handler._request_exec_summary(), request_time))


# 初始化
if not "g_http_server" in globals():
    g_http_server = None


def init_http_server(http_port=5088):
    global g_http_server
    if g_http_server:
        return

    g_http_server = CHttpServer(http_port)
    g_http_server.start()
