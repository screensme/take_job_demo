#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString

# 发送短信验证码post
class SendSmsHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++send sms+++++++++++')
        self.log.info(json.dumps(self.get_arguments()))
        mobile = self.get_argument('mobile')
        key = self.get_argument('key')
        cache_flag = self.get_cache_flag()
        result = yield self.db.Send_sms(mobile, key, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 校验短信验证码get
class VerifySmsHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, mobile, code):
        self.log.info('+++++++++++Verify sms+++++++++++')
        cache_flag = self.get_cache_flag()
        result = yield self.db.Verification_sms(mobile, code, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return
