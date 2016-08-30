#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString
import re

logger = logging.getLogger('boilerplate.' + __name__)

class better404(BaseHandler):

    def _write_404(self):
        result = {'status': 'fail',
                  'msg': 404,
                  'token': '',
                  'data': {}
                  }
        self.write(ObjectToString().encode(result))
        self.finish()
        return

    def get(self):
        self._write_404()

# 用户注册，手机号注册
class RegisterHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('user register')
        self.log.info(json.dumps(self.get_arguments()))
        cache_flag = self.get_cache_flag()
        data = dict()
        try:
            data['mobile'] = self.get_argument('mobile')
            data['pwd'] = self.get_argument('pwd')
            data['code'] = self.get_argument('code')
        except Exception, e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '缺少参数'
            result['data'] = {}

        if len(data['mobile']) != 11:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "登录手机号有误，请重新输入"
            result['data'] = {}

        else:
            result = yield self.db.Register_user(data['mobile'],
                                                 data['pwd'],
                                                 data['code'],
                                                 cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 用户登陆
class LoginHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('user login')
        self.log.info(json.dumps(self.get_arguments()))
        cache_flag = self.get_cache_flag()
        data = dict()
        try:
            data['mobile'] = self.get_argument('mobile')
            data['pwd'] = self.get_argument('pwd')
            #
            # data['mobibuild'] = self.get_argument('mobibuild')
            # data['mobitype'] = self.get_argument('mobitype')
        except Exception, e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '缺少用户名或密码'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        # try:
        #     data['umengid'] = self.get_argument('umengid')
        # except Exception, e:
        #     data['umengid'] = 'umengid/%s' % (self.get_argument('mobile'), )

        if len(data['mobile']) != 11:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "登录手机号有误，请重新输入"
            result['data'] = {}

        else:
            result = yield self.db.User_login(mobile=data['mobile'],
                                              pwd=data['pwd'],
                                              cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 登陆退出
class LogoutHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token=str):
        self.log.info('user logout')
        result = yield self.db.User_logout(token)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 忘记，找回密码
class ForgetpwdHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('user forget password')
        self.log.info(json.dumps(self.get_arguments()))
        data = dict()
        try:
            data['mobile'] = self.get_argument('mobile')
            data['pwd'] = self.get_argument('pwd')
            data['code'] = self.get_argument('code')
        except Exception,e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '缺少参数！'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        cache_flag = self.get_cache_flag()
        result = yield self.db.User_forgetpwd(data['mobile'],
                                              data['pwd'],
                                              data['code'],
                                              cache_flag=cache_flag
                                              )
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 修改密码
class UpdatePwdHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('user update password')
        self.log.info(json.dumps(self.get_arguments()))
        try:
            token = self.get_argument('token')
            oldpwd = self.get_argument('oldpwd')
            pwd = self.get_argument('pwd')
        except Exception,e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "缺少参数"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        cache_flag = self.get_cache_flag()

        if (oldpwd == '') or (pwd == ''):
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "输入的密码不能为空"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            self.log.info('user update false,pwd is None')
            return
        else:
            result = yield self.db.User_updatepwd(token=token,
                                                  oldpwd=oldpwd,
                                                  pwd=pwd,
                                                  cache_flag=cache_flag
                                                  )
            self.write(ObjectToString().encode(result))
        self.finish()
        return

# 个人信息页
class UserHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('user info')
        cache_flag = self.get_cache_flag()
        result = yield self.db.Home_user(token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 消息页,显示数量
class MessageHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('message number')
        self.log.info(json.dumps(self.get_arguments()))
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = 0
        else:
            result = yield self.db.Job_message(token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get全部
class MessageAllHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('get resume all status')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        else:
            result = yield self.db.Message_all(page, num, token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 简历状态查看get被查看
class MessageViewedHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('user view resume status viewed')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        else:
            result = yield self.db.Message_viewed(page, num, token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get简历通过
class MessageCommunicatedHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('user view resume status pass and info')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        else:
            result = yield self.db.Message_communicated(page, num, token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get面试通过
class MessagePassedHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('user view resume status passed')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        else:
            result = yield self.db.Message_passed(page, num, token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get不合适
class MessageImproperHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('user view resume status deny')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        else:
            result = yield self.db.Message_improper(page, num, token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 查看收藏get
class ViewcollectHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, page, num, token):
        self.log.info('user view collection job')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        else:
            result = yield self.db.view_user_collections(page, num, token, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 收藏和取消收藏职位post
class AddcollectHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('user add or del collections')
        self.log.info(json.dumps(self.get_arguments()))
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        job_id = self.get_argument('job_id')
        if re.match(r'\d+', '%s' % token):
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = 0
        else:
            result = yield self.db.user_add_collections(token, job_id, cache_flag=cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 取消收藏职位post(已不用)
class CutcollectHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info(json.dumps(self.get_arguments()))
        self.log.info('user cancel collections')
        cache_flag = self.get_cache_flag()
        data = dict()
        try:
            token = self.get_argument('token')
            data['job_id'] = self.get_argument('job_id')
        except Exception, e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '缺少参数'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return

        result = yield self.db.user_cancel_collections(token, data['job_id'], cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return
