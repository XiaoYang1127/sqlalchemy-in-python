#!/usr/bin/env/python
# _*_coding:utf-8_*_

import json
import threading

import httpserver.http_client as http_client


URL = "http://localhost:5088"


def do_user_test():
    add_class_by_sql_exp()

    count = 1
    for i in range(count):
        threading.Thread(target=add_user_by_sql_exp, args=(count,)).start()
    for i in range(count):
        threading.Thread(target=get_user_by_id, args=(count,)).start()
    for i in range(count):
        threading.Thread(target=query_user_by_id, args=(count,)).start()


def add_class_by_sql_exp():
    url = "%s/v1/api/user" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }

    post_data = {
        "method": "add_class_by_sql_exp"
    }
    http_client.http_request("post", url, headers=headers,
                             json=post_data, callback=test_http_back)


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
    http_client.http_request("post", url, headers=headers,
                             json=post_data, callback=test_http_back)


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
    http_client.http_request("post", url, headers=headers,
                             json=post_data, callback=test_http_back)


def get_user_by_id(i=1):
    url = "%s/v1/api/user?method=get_user_by_id" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }
    url = "%s&user_id=%d" % (url, i)
    http_client.http_request("get", url, headers=headers, callback=test_http_back)


def query_user_by_id(i=1):
    url = "%s/v1/api/user?method=query_user_by_id" % URL
    headers = {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }
    url = "%s&user_id=%d&tele=44568" % (url, i)
    http_client.http_request("get", url, headers=headers, callback=test_http_back)


def test_http_back(result, data):
    data = json.dumps(data, sort_keys=True, indent=2)
    print("\n\ntest_http_back result:%s data:%s" % (result, data))
