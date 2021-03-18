#!/usr/bin/env/python
# _*_coding:utf-8_*_

import json
import threading

import httpserver.http_client as http_client


URL = "http://localhost:5088"


def do_relationship_test():
    # add("add_one_to_many")
    # query("query_one_to_many")

    # add("add_one_to_one")
    # query("query_one_to_one")

    # add("add_many_to_many")
    query("query_many_to_many")


def headers():
    return {
        "content-type": "application/json",
        "secret_key": "secret_key",
    }


def add(method):
    url = "%s/v1/api/relationship" % URL
    post_data = {
        "method": method,
    }
    http_client.http_request("post", url, headers=headers(),
                             json=post_data, callback=on_response)


def query(method):
    url = "%s/v1/api/relationship" % URL
    post_data = {
        "method": method,
        "phone_id": 1,
        # "company_id": 1,
    }
    http_client.http_request("post", url, headers=headers(),
                             json=post_data, callback=on_response)


def on_response(result, data):
    data = json.dumps(data, sort_keys=True, indent=2)
    print("\n\non_response result:%s data:%s" % (result, data))
