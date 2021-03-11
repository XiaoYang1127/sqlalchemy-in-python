#!/usr/bin/env/python
# _*_coding:utf-8_*_

import threading

import httpserver.http_client as http_client


URL = "http://localhost:5088"


def do_user_test():
    count = 1
    add_class()
    for i in range(count):
        threading.Thread(target=add_user_by_sql_exp, args=(count,)).start()

    for i in range(count):
        threading.Thread(target=get_user_by_id, args=(count,)).start()


def add_class():
    url = "%s/v1/api/user" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }

    # add class
    post_data = {
        "method": "add_class"
    }
    http_client.http_request("post", url, headers=headers, json=post_data, callback=test_http_back)


def add_user_by_orm(i=1):
    url = "%s/v1/api/user" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }

    post_data = {
        "method": "add_user",
        "name": "liuliu_%d" % i,
        "age": 20 + i,
        "tele": 11234 + i,
        "addr": "guangzhou"
    }
    http_client.http_request("post", url, headers=headers, json=post_data, callback=test_http_back)


def add_user_by_sql_exp(i=1):
    url = "%s/v1/api/user" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }

    post_data = {
        "method": "add_user_by_sql_exp",
        "name": "caocao_%d" % i,
        "age": 40 + i,
        "tele": 44567 + i,
        "addr": "guangzhou"
    }
    http_client.http_request("post", url, headers=headers, json=post_data, callback=test_http_back)


def get_user_by_id(i=1):
    url = "%s/v1/api/user?method=get_user_by_id" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }
    url = "%s&user_id=%d" % (url, i)
    http_client.http_request("get", url, headers=headers, callback=test_http_back)


def test_http_back(result, data):
    print("test_http_back\n\tresult:%s data:%s" % (result, data))
