#!/usr/bin/env/python
# _*_coding:utf-8_*_

import time
import os
import sys
import traceback

import httpserver.http_server
import tests.start

RUN_MAIN = "main"
RUN_TEST = "test"
RUN_ALL = {RUN_MAIN, RUN_TEST}

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


def test():
    tests.start.do_unittest()


def process():
    while True:
        time.sleep(0.2)


if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        print("need a param in %s" % RUN_ALL)
        exit(0)

    if args[1] == RUN_MAIN:
        main()
    elif args[1] == RUN_TEST:
        test()
    else:
        print("param not in %s" % RUN_ALL)
