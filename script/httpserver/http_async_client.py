#!/usr/local/env python
# _*_ coding:utf-8 _*_

import json

import tornado.httpclient
from tornado.log import access_log


def http_request(method, url, callback=None, **kwargs):
    client = CHttpClient(method, url, **kwargs)
    if callback:
        client.set_callback(callback)
    client.start()


class CHttpClient(object):

    def __init__(self, method, url, **kwargs):
        self.m_method = method
        self.m_url = url
        self.m_retry = kwargs.pop("retry", 1)
        self.m_kwargs = kwargs

        self.m_callback = None

    def set_callback(self, callback):
        self.m_callback = callback

    def callback(self, result, content):
        if self.m_callback:
            self.m_callback(result, content)

    def start(self):
        while self.m_retry:
            try:
                async_client = tornado.httpclient.AsyncHTTPClient()
                request = tornado.httpclient.HTTPRequest(
                    self.m_url, method=self.m_method, **self.m_kwargs
                )
                async_client.fetch(
                    request,
                    callback=self.finish
                )
            except Exception as e:
                access_log.error("%s.run requst failed err_msg:%s" %
                                 (self.__class__.__name__, str(e)))
            finally:
                self.m_retry -= 1

    def finish(self, response):
        if not self.m_callback:
            return

        try:
            body = json.loads(response.body)
        except:
            body = response.body
        code = response.code
        if code == 200:
            self.m_callback(True, body)
        else:
            self.m_callback(False, body)
