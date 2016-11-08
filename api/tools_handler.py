#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString
import re


# 意见反馈post
class FeedbackHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Feedback+++++++++++')
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        info = self.get_argument('info')
        try:
            email = self.get_argument('email')
        except Exception,e:
            email = ''
        if info == '':
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '请输入反馈的内容'
            result['data'] = {'errorcode': 1000}
        else:
            result = yield self.db.Feed_back(token, info, email, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 获取版本,自动更新（仅Android）
class GetVersionHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Get Version+++++++++++')
        cache_flag = self.get_cache_flag()
        UserAgent = self.request.headers['User-Agent']
        device = 0 if "Mobile" in UserAgent or "Android" in UserAgent else 1
        # Version = self.get_argument('Version')
        if not device:
            Version = self.get_argument('Version')
            self.log.info(self.get_arguments())
            result = yield self.db.Get_Version(Version, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '非安卓手机'
            result['data'] = {'errorcode': 1000,
                              'isupdate': 0,
                              'version': '',
                              'update_url': ''}
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 申请成为校园代理post
class ApplicationProxyHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++ Application to proxy user +++++++++++')
        cache_flag = self.get_cache_flag()

        # token = self.get_argument('token')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.Application_proxy_user(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 新消息列表，包含所有消息数量
class MessageGetHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++ V1 Message, all message number +++++++++++')
        cache_flag = self.get_cache_flag()

        if re.match(r'\d+', '%s' % token):
            result = yield self.db.message_get(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 消息-话题进行中(1-->已预约,待同意，2-->已确认,待付款，3-已付款,待约见，)
class MessageTopicProcessHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++ V1 Message, all message number +++++++++++')
        cache_flag = self.get_cache_flag()

        if re.match(r'\d+', '%s' % token):
            result = yield self.db.message_topic_process(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 消息-话题待评价
class MessageTopicEvaluateHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++ V1 Message, all message number +++++++++++')
        cache_flag = self.get_cache_flag()

        if re.match(r'\d+', '%s' % token):
            result = yield self.db.message_topic_evaluate(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 消息-话题已完成
class MessageTopicFinishHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++ V1 Message, all message number +++++++++++')
        cache_flag = self.get_cache_flag()

        if re.match(r'\d+', '%s' % token):
            result = yield self.db.message_topic_finish(token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}

        self.write(ObjectToString().encode(result))
        self.finish()
        return
