#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from api.base_handler import BaseHandler
import tornado
from common.tools import args404, ObjectToString
import re


# 问答首页
class WorkplaceHomeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('+++++++++++问答首页 Full+++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.workplace_home(page, num, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 问答首页轮播图
class WorkplaceHomeSlideHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        self.log.info('+++++++++++问答首页轮播图 Full+++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.workplace_home_slide(cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 话题列表
class TopicListHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++问答首页 Full+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        page = self.get_argument('page')
        num = self.get_argument('num')
        field = self.get_argument('field')
        token = self.get_argument('token')

        result = yield self.db.topic_list(page, num, field, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 专家详情页
class ExpertFullHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, expert, token):
        self.log.info('+++++++++++问答首页 Full+++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.expert_full(expert, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 话题详情页
class TopicFullHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, topic, token):
        self.log.info('+++++++++++ company 500 +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.topic_full(topic, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 评价列表和详情页
class EvaluateGetHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, expert, token):
        self.log.info('+++++++++++ company 500 +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.evaluate_get(page, num, expert, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 写评价页
class EvaluateEditHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, topic):
        self.log.info('+++++++++++ company 500 +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.evaluate_edit_get(topic, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

    @gen.coroutine
    @tornado.web.asynchronous
    def post(self, topic):
        self.log.info('+++++++++++ company 500 +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        expert = self.get_argument('expert')
        evaluate = self.get_argument('evaluate')
        result = yield self.db.evaluate_edit(expert, topic, evaluate, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 预约页
class ReservationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ company 500 +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        time = self.get_argument('time')
        address = self.get_argument('address')
        question = self.get_argument('question')
        result = yield self.db.reservation(time, address, question, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 付款页
class WorkplacePayHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('+++++++++++ company 500 +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.workplace_pay(page, num, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 付款成功页
class WorkplacePaySuccessHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('+++++++++++ company 500 +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.workplace_pay_success(page, num, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

