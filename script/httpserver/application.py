#!/usr/bin/env/python
# _*_coding:utf-8_*_

import httpserver.handler
import logic.user_handler
import logic.relationship_handler


HANDLERS = [
    (r"/v1/api/user", logic.user_handler.CUserHandler),
    (r"/v1/api/relationship", logic.relationship_handler.CRelationshipHandler),
    (r"/.*", httpserver.handler.CRequestHandler),
]
