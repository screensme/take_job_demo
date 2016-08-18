#!/usr/bin/env python
# encoding: utf-8
from tornado import gen,web
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString
from database import Action

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
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user register')
        data = dict()
        try:
            data['mobile'] = self.get_argument('mobile')
            data['pwd'] = self.get_argument('pwd')
        except Exception,e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = e.log_message
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        isweb = 0
        id = None
        try:
            type = self.get_argument('get_type')
            id = self.get_argument('_id')
            if type == 'web':
                isweb = 1
        except Exception, e:
            isweb = 0
        cache_flag = self.get_cache_flag()

        if len(data['mobile']) != 11:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "登录手机号有误，请重新输入"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return

        else:
            if isweb == 0:
                result = yield Action.Register_user(data['mobile'],filepath,
                                                     data['pwd'],
                                                     cache_flag=cache_flag)
            self.write(ObjectToString().encode(result))
        self.finish()
        return


# 用户登陆
class LoginHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user login')
        data = dict()
        try:
            data['mobile'] = self.get_argument('mobile')
            data['pwd'] = self.get_argument('pwd')
            #
            # data['mobibuild'] = self.get_argument('mobibuild')
            # data['mobitype'] = self.get_argument('mobitype')
            isweb = 0
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
        try:
            type = self.get_argument('get_type')
            if type == 'web':
                isweb = 1
        except Exception, e:
            isweb = 0
        cache_flag = self.get_cache_flag()

        if len(data['mobile']) != 11:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "登录手机号有误，请重新输入"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return

        else:
            result = yield Action.User_login(mobile=data['mobile'],
                                             filepath=filepath,
                                              pwd=data['pwd'],
                                              # umengid=data['umengid'],
                                              # mobibuild=data['mobibuild'],
                                              # mobitype=data['mobitype'],
                                              cache_flag=cache_flag,
                                              isweb=int(isweb))
            self.write(ObjectToString().encode(result))
        self.finish()
        return

# 登陆退出
class LogoutHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token=str):
        filepath = self.settings['file_path']
        result = yield Action.User_logout(token,filepath)

        self.write(ObjectToString().encode(result))
        self.finish()

        return


# 忘记密码
class ForgetpwdHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        data = dict()
        try:
            data['mobile'] = self.get_argument('mobile')
            data['pwd'] = self.get_argument('pwd')
        except Exception,e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '缺少用户名或密码！'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        cache_flag = self.get_cache_flag()
        result = yield Action.User_forgetpwd(data['mobile'],filepath,
                                              data['pwd'],
                                              cache_flag=cache_flag
                                              )
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 修改密码
class UpdatePwdHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self, mobile=str):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user update password')
        data = dict()
        try:
            data['oldpwd'] = self.get_argument('oldpwd')
        except Exception,e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "缺少'oldpwd'"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        try:
            data['pwd'] = self.get_argument('pwd')
        except Exception,e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "缺少'pwd'"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        cache_flag = self.get_cache_flag()

        if (data['oldpwd'] == '') or (data['pwd'] == ''):
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = "输入的密码不能为空"
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            logger.info('user update false,pwd is None')
            return
        else:
            result = yield Action.User_updatepwd(mobile=mobile,
                                                 filepath=filepath,
                                                  oldpwd=data['oldpwd'],
                                                  pwd=data['pwd'],
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
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Home_user(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 消息页,显示数量
class MessageHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Job_message(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get全部
class MessageAllHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Message_all(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return


# 简历状态查看get被查看
class MessageViewedHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Message_viewed(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get待沟通
class MessageCommunicatedHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Message_communicated(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get面试通过
class MessagePassedHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Message_passed(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历状态查看get不合适
class MessageImproperHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        filepath = self.settings['file_path']
        logger.info(json.dumps(self.get_arguments(), indent=4))
        logger.info('user forget password')
        cache_flag = self.get_cache_flag()
        result = yield Action.Message_improper(token,filepath, cache_flag=cache_flag)
        self.write(ObjectToString().encode(result))
        self.finish()
        return
