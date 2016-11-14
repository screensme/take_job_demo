#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from api.base_handler import BaseHandler
import tornado
from common.tools import args404, ObjectToString
import re
import json

# ping++ id
Test_Secret_Key = "sk_test_jPK4GKWLOCW94av5i5nTmrjL"
Live_Secret_Key = "sk_live_X9ajj1TCa1u15Si94ObzLWDS"

pingpp_app_key = "app_eTiLm1mvTGe5O4mv"
pingpp_api_key = {'test_test': Test_Secret_Key,
                  'true_true': Live_Secret_Key}


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
        self.log.info('+++++++++++话题列表 Full+++++++++++')
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
        self.log.info('+++++++++++专家详情页 Full+++++++++++')
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
        self.log.info('+++++++++++ 话题详情页 TopicFull +++++++++++')
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
        self.log.info('+++++++++++ 评价列表和详情页 Evaluate +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.evaluate_get(page, num, expert, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 写评价页
class EvaluateEditHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        self.log.info('+++++++++++ 写评价页 Evaluate Edit get +++++++++++')
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        reservation_id = self.get_argument('reservation_id')
        result = yield self.db.evaluate_edit_get(reservation_id, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ 写评价页 Evaluate Edit post +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        reservation_id = self.get_argument('reservation_id', '')
        score = self.get_argument('score')
        evaluate = self.get_argument('evaluate')
        result = yield self.db.evaluate_edit_post(reservation_id, score, evaluate, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 预约页
class ReservationHandler(BaseHandler):
    # @gen.coroutine
    # @tornado.web.asynchronous
    # def get(self):  # 已经不用了
    #     self.log.info('+++++++++++ Reservation 预约 GET +++++++++++')
    #     self.log.info(self.get_arguments())
    #     cache_flag = self.get_cache_flag()
    #     token = self.get_argument('token')
    #     topic_id = self.get_argument('topic_id')
    #     # expert_id = self.get_argument('expert_id')
    #     result = yield self.db.reservation_get(topic_id, token, cache_flag)
    #
    #     self.write(ObjectToString().encode(result))
    #     self.finish()
    #     return

    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ Reservation 预约 POST start +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        meet_message = self.get_argument('meet_message')
        meet_question = self.get_argument('meet_question')
        topic_id = self.get_argument('topic_id')
        expert_id = self.get_argument('expert_id')
        result = yield self.db.reservation(topic_id, expert_id, meet_message, meet_question, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 付款页
class WorkplacePayHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++ 付款页 200 +++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()

        pingxx_secret_key = pingpp_api_key['true_true']
        ip = self.request.remote_ip
        token = self.get_argument('token')
        pay_type = self.get_argument('pay_type')
        # money = self.get_argument('money')
        topic_id = self.get_argument('topic_id')
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.workplace_pay(pingpp_app_key, pingxx_secret_key, topic_id,
                                                 pay_type, ip, token, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 付款成功页
class WorkplacePaySuccessHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, message_id, token):
        self.log.info('+++++++++++ 付款成功页 200 +++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.workplace_pay_success(message_id, token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 支付返回结果，ping++返回结果
class WorkplacePayResultHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info("--------------------------------- ping ++ receive charge result....")
        self.log.info(self.request.body)
        form = json.loads(self.request.body)
        self.log.info(json.dumps(form, indent=4))
        cache_flag = self.get_cache_flag()
        result = yield self.db.recv_charge(charge=form, cache_flag=cache_flag)
        self.log.info('charge is save OK')
        self.write('success')
        self.finish()
        return

        # # test charge
        # from test.test_action import test_charge
        # form = test_charge.form   # 测试用的订单
        # cache_flag = self.get_cache_flag()
        # result = yield self.db.recv_charge(charge=form, cache_flag=cache_flag)
        # self.log.info('test charge is save OK')
        # self.write('test success')
        # self.finish()
        # return
