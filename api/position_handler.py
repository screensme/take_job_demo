#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from tornado import web
import json
from api.base_handler import BaseHandler
import tornado
from common.tools import args404, ObjectToString


# 首页
class HomeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        cache_flag = self.get_cache_flag()
        self.log.info('+++++++++++Home page+++++++++++')
        result = yield self.db.Home_info(page, num, token, cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 首页搜索职位
class SearchHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Search+++++++++++')
        self.log.info(self.get_arguments())
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

# 搜索公司
class SearchCompanyHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Search Company+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        # page = self.get_argument('page')
        # num = self.get_argument('num')
        values = self.get_arguments()
        if 'company_name' not in values:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '请输入搜索内容!'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        result = yield self.db.Search_company(values, cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 搜索公司或者职位
class SearchCompanyOrJobHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Search Company Or Job+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        last = self.get_arguments()
        if 'company_name' not in last:
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

# 职位推荐
class RecommendjobHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Recommend job+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        result = yield self.db.Recommend_job(token, page, num, cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 急速招聘
class SpeedjobHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Speed job+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        try:
            job_type = self.get_argument('job_type')
        except Exception, e:
            job_type = 'fulltime'
        result = yield self.db.Speed_job(token, job_type, page, num, cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 职位详情get
class PositionHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, job_id, token):
        self.log.info('+++++++++++Position Full+++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.Position_full(job_id, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 热门搜索
class HostsearchlistHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++Hot search+++++++++++')
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
        self.log.info('+++++++++++Hot city+++++++++++')
        cache_flag = self.get_cache_flag()
        data = dict()
        data['hotcity'] = ['不限', '北京', '上海', '广州','深圳']
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = data

        self.write(ObjectToString().encode(result))
        self.finish()
        return
