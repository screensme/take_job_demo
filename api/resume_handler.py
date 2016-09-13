#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
from api.base_handler import BaseHandler
import re
import tornado
from common.tools import args404, ObjectToString

# 简历查看get
class ResumeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        self.log.info('+++++++++++Resume get+++++++++++')
        cache_flag = self.get_cache_flag()
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.Resume_view(token, cache_flag)

        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历投递post
class PostresumeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Post+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        try:
            token = self.get_argument('token')
            job_id = self.get_argument('job_id')
        except Exception, e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '未登录状态'
            result['data'] = {}
            self.write(ObjectToString().encode(result))
            self.finish()
            return
        if re.match(r'\d+', '%s' % token):
            result = yield self.db.Post_resume(token, job_id, cache_flag)
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '未登录状态'
            result['data'] = {}
        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-基本信息post
class ResumeBasicHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume edit+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        basic = self.get_argument('basic')
        # data['education'] = self.get_argument('education')
        # data['birthday'] = self.get_argument('birthday')
        # data['politics_status'] = self.get_argument('politics_status')
        # data['gender'] = self.get_argument('gender')
        # data['current_area'] = self.get_argument('current_area')
        # data['name'] = self.get_argument('name')
        # data['phonenum'] = self.get_argument('phonenum')
        # data['email'] = self.get_argument('email')
        # # data['avatar'] = self.get_argument('avatar')
        # data['marital_status'] = self.get_argument('marital_status')

        result = yield self.db.Resume_Basic(token, basic, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-教育经历post
class ResumeEducationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume education+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        # data = dict()
        education = self.get_argument('education')
        # data['school'] = self.get_argument('school')
        # data['major'] = self.get_argument('major')
        # data['start_time'] = self.get_argument('start_time')
        # data['end_time'] = self.get_argument('end_time')
        # data['degree'] = self.get_argument('degree')

        result = yield self.db.Resume_Education(token, education, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-职业意向post
class ResumeExpectHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Expect+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        # data = dict()
        expect = self.get_argument('expect')
        # data['area'] = self.get_argument('area')
        # data['title'] = self.get_argument('title')
        # data['status'] = self.get_argument('status')
        # data['trade'] = self.get_argument('trade')
        # data['expect_salary'] = self.get_argument('expect_salary')

        result = yield self.db.Resume_Expect(token, expect, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-实习经历post
class ResumeCareerHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Career+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        career = self.get_argument('career')
        # data['duty'] = self.get_argument('duty')
        # data['area'] = self.get_argument('area')
        # data['start_time'] = self.get_argument('start_time')
        # data['title'] = self.get_argument('title')
        # data['trade'] = self.get_argument('trade')
        # data['end_time'] = self.get_argument('end_time')
        # data['company'] = self.get_argument('company')
        result = yield self.db.Resume_Career(token, career, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-项目社会实践post(暂时不用)
class ResumeExperienceHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Experience+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        # data['item_name'] = self.get_argument('item_name')
        # data['item_duty'] = self.get_argument('item_duty')
        # data['start_year3'] = self.get_argument('start_year3')
        # data['start_month3'] = self.get_argument('start_month3')
        # data['end_year3'] = self.get_argument('end_year3')
        # data['end_month3'] = self.get_argument('end_month3')
        # data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-校内职务post(暂时不用)
class ResumeSchooljobHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume School job+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        # data['item_name'] = self.get_argument('item_name')
        # data['item_duty'] = self.get_argument('item_duty')
        # data['start_year3'] = self.get_argument('start_year3')
        # data['start_month3'] = self.get_argument('start_month3')
        # data['end_year3'] = self.get_argument('end_year3')
        # data['end_month3'] = self.get_argument('end_month3')
        # data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-校内奖励post(暂时不用)
class ResumeSchoolRewardsHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume School Rewards+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        # data['item_name'] = self.get_argument('item_name')
        # data['item_duty'] = self.get_argument('item_duty')
        # data['start_year3'] = self.get_argument('start_year3')
        # data['start_month3'] = self.get_argument('start_month3')
        # data['end_year3'] = self.get_argument('end_year3')
        # data['end_month3'] = self.get_argument('end_month3')
        # data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-语言能力post(暂时不用)
class ResumeLanguagesHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Languages+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        # data['item_name'] = self.get_argument('item_name')
        # data['item_duty'] = self.get_argument('item_duty')
        # data['start_year3'] = self.get_argument('start_year3')
        # data['start_month3'] = self.get_argument('start_month3')
        # data['end_year3'] = self.get_argument('end_year3')
        # data['end_month3'] = self.get_argument('end_month3')
        # data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-IT技能post(暂时不用)
class ResumeSkillHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Skill+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        # data['item_name'] = self.get_argument('item_name')
        # data['item_duty'] = self.get_argument('item_duty')
        # data['start_year3'] = self.get_argument('start_year3')
        # data['start_month3'] = self.get_argument('start_month3')
        # data['end_year3'] = self.get_argument('end_year3')
        # data['end_month3'] = self.get_argument('end_month3')
        # data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-获得证书post(暂时不用)
class ResumeCertificateHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Certificate+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        # data['item_name'] = self.get_argument('item_name')
        # data['item_duty'] = self.get_argument('item_duty')
        # data['start_year3'] = self.get_argument('start_year3')
        # data['start_month3'] = self.get_argument('start_month3')
        # data['end_year3'] = self.get_argument('end_year3')
        # data['end_month3'] = self.get_argument('end_month3')
        # data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-自我评价post
class ResumeEvaluationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Evaluation+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['description'] = self.get_argument('description')

        result = yield self.db.Resume_Evaluation(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-修改头像post
class ResumeAvatarHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Resume Avatar+++++++++++')
        self.log.info(self.get_arguments())
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        avatar = self.get_argument('avatar')

        result = yield self.db.Resume_Avatar(token=token, avatar=avatar, cache_flag=cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return
