#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib import urlencode
from configs.web_config import API_KEY

class SmsApi(object):

    def __init__(self):
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'
        }
        self.apikey = API_KEY
        # self.logger = init_log(debug=app.config.get('DEBUG', True))

    # 注册接口
    def sms_register(self, mobile, rand_num):
        single_url = "https://sms.yunpian.com/v2/sms/single_send.json"
        kwargs = {}
        kwargs['apikey'] = self.apikey
        kwargs['mobile'] = mobile
        text = "【招聘头条】您的验证码为：%s，请在页面中输入以完成注册，上招聘头条找好工作。" % (rand_num,)
        kwargs['text'] = text
        try:
            r = requests.post(single_url, data=urlencode(kwargs),
                              headers=self.headers)
            return r.json()
        except Exception as e:
            # self.log.info.exception(e)
            ret = {'code': 500}
            return ret

    # 忘记密码
    def sms_forget(self, mobile, rand_num):
        single_url = "https://sms.yunpian.com/v2/sms/single_send.json"
        kwargs = {}
        kwargs['apikey'] = self.apikey
        kwargs['mobile'] = mobile

        text = "【招聘头条】您的验证码为：%s，请在页面中输入以找回密码，上招聘头条找好工作。" % (rand_num,)
        kwargs['text'] = text
        try:
            r = requests.post(single_url, data=urlencode(kwargs),
                              headers=self.headers)
            return r.json()
        except Exception as e:
            # self.logger.exception(e)
            ret = {'code': 500}
            return ret

    # 短信通知面试邀请
    def sms_invite(self, mobile, content):
        single_url = "https://sms.yunpian.com/v2/sms/single_send.json"
        kwargs = {}
        kwargs['apikey'] = self.apikey
        kwargs['mobile'] = mobile

        kwargs['text'] = content
        try:
            r = requests.post(single_url, data=urlencode(kwargs),
                              headers=self.headers)
            return r.json()
        except Exception as e:
            # self.logger.exception(e)
            ret = {'code': 500}
            return ret
