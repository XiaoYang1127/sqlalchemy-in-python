#!/usr/bin/env/python
# _*_coding:utf-8_*_

import httpserver.handler
import logic.user_handler


HANDLERS = [
    (r"/v1/api/user", logic.user_handler.CUserHandler),
    (r"/.*", httpserver.handler.CRequestHandler),
]
