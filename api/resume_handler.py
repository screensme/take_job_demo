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
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        data = dict()
        token = self.get_argument('token')
        cao = self.get_arguments()
        data['education'] = self.get_argument('education')
        data['birthday'] = self.get_argument('birthday')
        data['politics_status'] = self.get_argument('politics_status')
        data['gender'] = self.get_argument('gender')
        data['current_area'] = self.get_argument('current_area')
        data['name'] = self.get_argument('name')
        data['phonenum'] = self.get_argument('phonenum')
        data['email'] = self.get_argument('email')
        # data['avatar'] = self.get_argument('avatar')
        data['marital_status'] = self.get_argument('marital_status')

        result = yield self.db.Resume_Basic(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-教育经历post
class ResumeEducationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['school'] = self.get_argument('school')
        data['major'] = self.get_argument('major')
        data['start_time'] = self.get_argument('start_time')
        data['end_time'] = self.get_argument('end_time')
        data['degree'] = self.get_argument('degree')

        result = yield self.db.Resume_Education(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-职业意向post
class ResumeExpectHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['area'] = self.get_argument('area')
        data['title'] = self.get_argument('title')
        data['status'] = self.get_argument('status')
        data['trade'] = self.get_argument('trade')
        data['expect_salary'] = self.get_argument('expect_salary')

        result = yield self.db.Resume_Expect(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-实习经历post
class ResumeExperienceHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['gs'] = self.get_argument('gs')
        data['end_time'] = self.get_argument('end_time')
        data['start_time'] = self.get_argument('start_time')
        data['school_name'] = self.get_argument('school_name')
        data['job_info'] = self.get_argument('job_info')
        data['job_name'] = self.get_argument('job_name')
        result = yield self.db.Resume_Experience(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-项目实践post
class ResumeItemHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
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
        result = yield self.db.Resume_Item(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 简历编辑-自我评价post
class ResumeEvaluationHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        # filepath = self.settings['file_path']
        cache_flag = self.get_cache_flag()
        token = self.get_argument('token')
        data = dict()
        data['description'] = self.get_argument('description')

        result = yield self.db.Resume_Evaluation(token, data, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return