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
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        last = self.get_arguments()
        if 'job_name' not in last:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '请输入搜索内容!'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        result = yield self.db.Search_job(last, token, page, num, cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()

        return

# 意见反馈post
class FeedbackHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
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
        cache_flag = self.get_cache_flag()
        # token = self.get_argument('token')
        # company_id = self.get_argument('company_id')
        result = yield self.db.Position(job_id, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()

        return

# 首页搜索
class HostsearchlistHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        cache_flag = self.get_cache_flag()
        # token = self.get_argument('token')
        # page = self.get_argument('page')
        # num = self.get_argument('num')
        # last = self.get_arguments()
        result = yield self.db.Host_search_list(cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()

        return

# 热门搜索城市列表(先写4个)get
class HotcityHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        cache_flag = self.get_cache_flag()
        data = dict()
        data['hotcity'] = ['北京','上海','广州','深圳']
        result = dict()
        result['status'] = 'fail'
        result['token'] = token
        result['msg'] = ''
        result['data'] = data

        self.write(ObjectToString().encode(result))
        self.finish()

        return