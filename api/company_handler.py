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
    def post(self):
        # filepath = self.settings['file_path']
        token = self.get_argument('token')
        company_id = self.get_argument('company_id')
        result = yield self.db.Company_full(token,company_id)

        self.write(ObjectToString().encode(result))
        self.finish()

        return