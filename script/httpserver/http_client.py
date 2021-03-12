#!/usr/local/env python
# _*_ coding:utf-8 _*_

from tornado.log import access_log

import threading
import requests


def http_request(method, url, callback=None, **kwargs):
    client = CHttpClient(method, url, **kwargs)
    if callback:
        client.set_callback(callback)
    client.start()


class CHttpClient(threading.Thread):

    def __init__(self, method, url, **kwargs):
        threading.Thread.__init__(self)
        self.m_method = method
        self.m_url = url
        self.m_retry = kwargs.pop("retry", 1)
        self.m_kwargs = kwargs

        self.m_callback = None

        self.m_result = False
        self.m_content = {}

    def set_callback(self, callback):
        self.m_callback = callback

    def callback(self, result, content):
        if self.m_callback:
            self.m_callback(result, content)

    def run(self):
        """
        :param method: get/post/put/delete/head/options
        :param url: 请求的地址
        :param params: 可以是字典，可以是字符串，可以是字节
        :param data: 可以是字典，可以是字符串，可以是字节, 可以是文件对象
        :param json: 将json中对应的数据进行序列化成一个字符串，发送到服务器端的body中
        :param headers: 发送请求头到服务器端
            - 文件操作，"Content-Type": "application/form-data",
            - json请求，"content-type": "application/json"
        :param cookies: 发送Cookie到服务器端
        :param files: 发送文件
        :param proxies: 代理地址，字典类型，key为协议，value为地址
            - "http": "61.172.249.96:80",
        :return:
        """
        while self.m_retry:
            try:
                response = requests.request(
                    self.m_method, self.m_url, **self.m_kwargs)
                self.m_result = True
                self.m_content = response.json()
            except Exception as e:
                access_log.error("%s.run requst failed err_msg:%s" %
                                 (self.__class__.__name__, str(e)))
            finally:
                self.m_retry -= 1

        self.finish()

    def finish(self):
        if not self.m_result:
            access_log.error(
                "%s.finish failed url:%s content:%s" %
                (self.__class__.__name__, self.m_url, self.m_content))

        self.callback(self.m_result, self.m_content)
