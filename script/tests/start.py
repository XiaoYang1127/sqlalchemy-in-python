#!/usr/bin/env/python
# _*_coding:utf-8_*_

import tests.user_test
import tests.relationship_test
import tests.sql_safe_test


def do_unittest():
    # tests.user_test.do_user_test()
    # tests.relationship_test.do_relationship_test()
    tests.sql_safe_test.do_sql_test()
