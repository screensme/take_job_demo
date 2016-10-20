#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from tornado import web
import json
from api.base_handler import BaseHandler
import tornado
from common.tools import args404, ObjectToString
import re


# 首页
class HomeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        cache_flag = self.get_cache_flag()
        self.log.info('+++++++++++Home page+++++++++++')
        result = yield self.db.Home_info(page, num, token, cache_flag=cache_flag)
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
        # token = self.get_argument('token')
        # page = self.get_argument('page')
        # num = self.get_argument('num')
        last = self.get_arguments()
        if ('job_name' not in last) or ('job_name' == ''):
            page = last['page']
            num = last['num']
            token = last['token']
            result = yield self.db.Home_info(page, num, token, last, cache_flag)
        else:
            result = yield self.db.Search_job(last, cache_flag,)

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
        value = self.get_arguments()
        result = yield self.db.Speed_job(value, cache_flag,)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 职为你来post
class JobForMeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Job For Me +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        result = yield self.db.Job_For_Me(token, page, num, cache_flag,)

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
        # cache_flag = self.get_cache_flag()
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


# 活动列表get
class ActivityListGetHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        self.log.info('+++++++++++ Activity List +++++++++++')
        cache_flag = self.get_cache_flag()

        result = yield self.db.Activity_List(cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 活动post(显示company/显示job)
class ActivityHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Activity info +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        active_id = self.get_argument('active_id')
        token = self.get_argument('token')
        key_type = self.get_argument('key_type')
        company_id = self.get_argument('company_id')
        page = self.get_argument('page')
        num = self.get_argument('num')
        if key_type == 'company':
            result = yield self.db.Activity_Company(active_id, token, page, num, cache_flag)
        else:
            result = yield self.db.Activity_Job(active_id, token, page, num, company_id, cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# -----------------------------------职业导航---start------------------
# 职业导航
class ProNavigationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Professional navigation !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.pro_navigation_list(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 行业职位排行榜
class RankTradeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Ranking Trade !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        trade = self.get_argument('trade', '')
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.rank_trade(trade, token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 高薪职位排行榜
class RankHighSalaryHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Ranking HighSalary !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.Rank_high_salary(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 热门职位排行榜
class RankHotJobHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Ranking HotJob !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.rank_hot_job(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 工资走势图
class SalaryTrendHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ salary_trend_list !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        job = self.get_argument('job', '')
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.salary_trend_list(job, token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 工资区间图
class SalaryTantileHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ salary_tantile_list !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        job = self.get_argument('job', '')
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.salary_tantile_list(job, token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 学历分布图
class EduTantileHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ edu_tantile_list !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        job = self.get_argument('job', '')
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.edu_tantile_list(job, token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 工作年限分布图
class ExpTantileHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ exp_tantile_list !!! +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        job = self.get_argument('job', '')
        token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.exp_tantile_list(job, token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return
# -----------------------------------职业导航---end------------------