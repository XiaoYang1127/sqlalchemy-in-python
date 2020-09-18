#!/usr/bin/env/python
# _*_coding:utf-8_*_

import os

import tornado.gen
import tornado.escape

import commons
import commondefs
import httpserver.base


class CRequestHandler(httpserver.base.CBaseHandler):
    HTTP_AUTH = "secret_key"

    def is_valid_request(self):
        if self.request.method not in ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]:
            self.simple_response(405)
            return 0

        if self.get_headers("secret_key") != self.HTTP_AUTH:
            self.simple_response(401)
            return 0

        return 1

    @tornado.gen.coroutine
    def prepare(self):
        if not self.is_valid_request():
            return

        if self.request.method == "GET":
            for key in self.request.query_arguments.keys():
                self.m_query_params[key.lower()] = self.get_query_argument(key)
        else:
            content_type = self.request.headers.get("Content-Type", "")
            if not content_type:
                self.simple_response(412)
                return

            if content_type.startswith("application/json"):
                try:
                    json_body = tornado.escape.json_decode(self.request.body)
                    for k, v in json_body.items():
                        self.m_query_params[k.lower()] = v
                except:
                    self.simple_response(500, "body json decoded fail")
                    return
            else:
                for key in self.request.body_arguments.keys():
                    self.m_query_params[key.lower()] = self.get_body_argument(key)

                self.check_save_file()

    def check_save_file(self):
        files = self.request.files.get("files", [])
        if not files:
            return

        upload_path = commondefs.UPLOAD_PATH
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        files_data = files[0]
        client_name = files_data["filename"]
        content = files_data["body"]

        file_ext = os.path.splitext(client_name)[1][1:]
        filename = "%s.%s" % (commons.MD5(content), file_ext)
        save_path = os.path.join(upload_path, filename)

        if os.path.exists(save_path):
            return

        with open(save_path, mode="wb") as fp:
            fp.write(content)
            fp.close()
