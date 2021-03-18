#!/usr/bin/env/python
# _*_coding:utf-8_*_

import json
import threading

import httpserver.http_client as http_client


URL = "http://localhost:5088"


def do_user_test():
    i = 1
    add_class_by_sql_exp(i)
    add_user_by_sql_exp(i)
    add_user_by_orm(i)


def headers():
    return {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }


def add_class_by_sql_exp(i):
    url = "%s/v1/api/user" % URL
    post_data = {
        "method": "add_class_by_sql_exp",
        "name": "class_%s" % i
    }
    http_client.http_request("post", url, headers=headers(),
                             json=post_data, callback=on_response)


def add_user_by_orm(i):
    url = "%s/v1/api/user" % URL
    post_data = {
        "method": "add_user",
        "class_id": 1,
        "name": "orm_liuliu_%d" % i,
        "age": 20 + i,
        "tele": 11234 + i,
        "addr": "guangzhou"
    }
    http_client.http_request("post", url, headers=headers(),
                             json=post_data, callback=on_response)


def add_user_by_sql_exp(i):
    url = "%s/v1/api/user" % URL
    post_data = {
        "method": "add_user_by_sql_exp",
        "class_id": 1,
        "name": "caocao_%d" % i,
        "age": 40 + i,
        "tele": 44567 + i,
        "addr": "guangzhou"
    }
    http_client.http_request("post", url, headers=headers(),
                             json=post_data, callback=on_response)


def get_user_by_id(i=1):
    url = "%s/v1/api/user?method=get_user_by_id" % URL
    url = "%s&user_id=%d" % (url, i)
    http_client.http_request("get", url, headers=headers(), callback=on_response)


def query_user_by_id(i=1):
    url = "%s/v1/api/user?method=query_user_by_id" % URL
    url = "%s&user_id=%d&tele=44568" % (url, i)
    http_client.http_request("get", url, headers=headers(), callback=on_response)


def on_response(result, data):
    data = json.dumps(data, sort_keys=True, indent=2)
    print("\n\non_response result:%s data:%s" % (result, data))
