#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from tornado import web
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString
from database import Action


# 首页
class HomeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        # token = self.get_argument('token')
        result = yield self.db.Home(page, num, token, cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()

        return

# 首页搜索
class SearchHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        last = self.get_arguments()
        result = yield self.db.Search_job(last, token, page, num, cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()

        return

# 意见反馈post
class FeedbackHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['email'] = self.get_argument('email')
        data['info'] = self.get_argument('info')
        result = yield self.db.Feed_back(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()

        return

# 职位详情get
class PositionHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, job_id, token):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        # token = self.get_argument('token')
        # company_id = self.get_argument('company_id')
        result = yield self.db.Position(job_id, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()

        return
