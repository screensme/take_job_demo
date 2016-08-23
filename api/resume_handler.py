#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
from api.base_handler import BaseHandler
import logging
import tornado
from common.tools import args404, ObjectToString
from database import Action

# 职位详情get
class ResumeHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, token):
        # token = self.get_argument('token')
        cache_flag = self.get_cache_flag()
        result = yield self.db.Resume_view(token, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-基本信息post
class ResumeBasicHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        data = dict()
        token = self.get_argument('token')
        data['user_image'] = self.get_argument('user_image')
        data['name'] = self.get_argument('name')
        data['sex'] = self.get_argument('sex')
        data['education'] = self.get_argument('education')
        data['marriage'] = self.get_argument('marriage')
        data['education'] = self.get_argument('education')
        data['polity_face'] = self.get_argument('polity_face')
        data['email'] = self.get_argument('email')
        data['birth_year'] = self.get_argument('birth_year')
        data['mobile'] = self.get_argument('mobile')
        data['place'] = self.get_argument('place')
        result = yield self.db.Resume_Basic(token,filepath, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-教育经历post
class ResumeEducationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['school'] = self.get_argument('school')
        data['major'] = self.get_argument('major')
        data['start_year'] = self.get_argument('start_year')
        data['start_month'] = self.get_argument('start_month')
        data['end_year'] = self.get_argument('end_year')
        data['end_month'] = self.get_argument('end_month')
        data['education2'] = self.get_argument('education2')
        result = yield self.db.Resume_Education(token,filepath, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-职业意向post
class ResumeExpectHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['expect_job'] = self.get_argument('expect_job')
        data['work_state'] = self.get_argument('work_state')
        data['expect_city'] = self.get_argument('expect_city')
        data['expect_salary'] = self.get_argument('expect_salary')
        data['expect_trade'] = self.get_argument('expect_trade')
        result = yield self.db.Resume_Expect(token,filepath, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-实习经历post
class ResumeExperienceHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['gs'] = self.get_argument('gs')
        data['gs_trade'] = self.get_argument('gs_trade')
        data['gs_job'] = self.get_argument('gs_job')
        data['gs_address'] = self.get_argument('gs_address')
        data['start_year2'] = self.get_argument('start_year2')
        data['start_month2'] = self.get_argument('start_month2')
        data['end_year2'] = self.get_argument('end_year2')
        data['end_month2'] = self.get_argument('end_month2')
        data['job_duty'] = self.get_argument('job_duty')
        result = yield self.db.Resume_Experience(token,filepath, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-项目实践post
class ResumeItemHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['item_name'] = self.get_argument('item_name')
        data['item_duty'] = self.get_argument('item_duty')
        data['start_year3'] = self.get_argument('start_year3')
        data['start_month3'] = self.get_argument('start_month3')
        data['end_year3'] = self.get_argument('end_year3')
        data['end_month3'] = self.get_argument('end_month3')
        data['item_des'] = self.get_argument('item_des')
        result = yield self.db.Resume_Item(token,filepath, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-自我评价post
class ResumeEvaluationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['school'] = self.get_argument('school')
        data['major'] = self.get_argument('major')
        data['start_year'] = self.get_argument('start_year')
        data['start_month'] = self.get_argument('start_month')
        data['end_year'] = self.get_argument('end_year')
        data['end_month'] = self.get_argument('end_month')
        data['education2'] = self.get_argument('education2')
        result = yield self.db.Resume_Evaluation(token,filepath, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return