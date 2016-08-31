#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from tornado import web
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString

# 修改数据，慎用
class EditdatabaseHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        cache_flag = self.get_cache_flag()
        if token == "123QWEqwe":
            result = yield self.db.Edit_datebase(cache_flag,)
        else:
            result = "no things don\'t BB!"
        self.write(ObjectToString().encode(result))
        self.finish()
        return