#!/usr/bin/env/python
# _*_coding:utf-8_*_

import time
import os
import sys
import traceback

from tornado.options import define, parse_command_line

import httpserver.http_server
import tests.start


script_path = "script"
if script_path not in sys.path:
    sys.path.append(script_path)


def init_log():
    '''
    Tornado uses three logger streams:

    - tornado.access: Per-request logging for Tornado's HTTP servers (and
        potentially other servers in the future)
    - tornado.application: Logging of errors from application code (i.e.
        uncaught exceptions from callbacks)
    - tornado.general: General-purpose logging, including any errors
        or warnings from Tornado itself.
    '''
    log_name = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    define('log_file_prefix', default='../%s.log' % log_name)
    define('log_rotate_mode', default='time')
    define('log_rotate_when', default='midnight')
    define('log_file_num_backups', default=90)
    define('log_rotate_interval', default=1)
    # define('logging', default="debug")  # already define "log"
    define('log_to_stderr', default=True)
    parse_command_line()


def base_init():
    init_log()


def main():
    try:
        base_init()
        httpserver.http_server.init_http_server()
    except Exception:
        traceback.print_exc()

    process()


def process():
    while True:
        time.sleep(0.001)


def test():
    tests.start.do_unittest()


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("python main.py main|test")
        exit(0)

    if argv[1] == "main":
        main()
    elif argv[1] == "test":
        test()
    else:
        print("python main.py main|test")
