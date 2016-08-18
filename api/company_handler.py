#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString
from database import Action

# 公司详情
class CompanyHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token=str):
        filepath = self.settings['file_path']
        result = yield Action.Company_full(token,filepath)

        self.write(ObjectToString().encode(result))
        self.finish()

        return