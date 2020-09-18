#!/usr/bin/env/python
# _*_coding:utf-8_*_

import hashlib


def MD5(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.md5(data).hexdigest()
