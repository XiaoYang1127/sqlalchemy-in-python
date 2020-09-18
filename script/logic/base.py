#!/usr/local/env python
# _*_ coding:utf-8 _*_

import httpserver.handler


class CBase(httpserver.handler.CRequestHandler):

    def update_model(self, model, update_data):
        b_update = False
        columns = model.tbl_cols()
        for k, v in update_data.items():
            if k not in columns:
                continue
            if getattr(model, k, None) == v:
                continue
            b_update = True
            setattr(model, k, v)
        return b_update
