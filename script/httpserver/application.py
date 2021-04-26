#!/usr/bin/env/python
# _*_coding:utf-8_*_

import httpserver.handler
import logic.user_handler
import logic.relationship_handler
import logic.parser_sql_handler
import logic.orm_config_handler


HANDLERS = [
    (r"/v1/api/user", logic.user_handler.CUserHandler),
    (r"/v1/api/relationship", logic.relationship_handler.CRelationshipHandler),
    (r"/v1/api/sql", logic.parser_sql_handler.CParserSqlHandler),
    (r"/v1/api/config", logic.orm_config_handler.COrmHandler),
    (r"/.*", httpserver.handler.CRequestHandler),
]
