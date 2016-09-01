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
            code = self.get_argument('code')
            if code == '我要修改数据':
                result = yield self.db.Edit_datebase(code, cache_flag,)
            else:
                result = "少废话，放码过来"
        else:
            result = "no things don\'t BB!"
        self.write(ObjectToString().encode(result))
        self.finish()
        return