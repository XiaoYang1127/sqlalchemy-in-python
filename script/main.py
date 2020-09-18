#!/usr/bin/env/python
# _*_coding:utf-8_*_

import time
import os
import sys
import traceback

import httpserver.http_server


script_path = "script"
if script_path not in sys.path:
    sys.path.append(script_path)


def base_init():
    httpserver.http_server.init_http_server()


def main():
    try:
        base_init()
    except:
        traceback.print_exc()

    process()


def process():
    while True:
        time.sleep(0.2)


# if __name__ == "__main__":
#     main()
