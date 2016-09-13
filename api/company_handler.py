#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
from api.base_handler import BaseHandler
import tornado
from common.tools import args404, ObjectToString

# 公司详情-公司信息get
class CompanyBasicHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, company_id, token):
        self.log.info('+++++++++++Company Full+++++++++++')
        if company_id[:1] == '0':
            company = {'company_name': '',
                       'company_trade': '',
                       'company_scale': '',
                       'company_type': '',
                       'company_site': '',
                       'company_logo': ''
                       }
            result = dict()
            result['status'] = 'success'
            result['token'] = token
            result['msg'] = ''
            result['data'] = company
        else:
            result = yield self.db.Company_basic(company_id, token)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 公司详情-企业详情get（公司介绍，大事记）
class CompanyCompanyHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def get(self, company_id, token):
        self.log.info('+++++++++++Company all job+++++++++++')
        if company_id[:1] == '0':
            company = {'company_id': '',
                       'company_des': '',
                       'boon': '',
                       'events': '',
                       'company_address': '',
                       'picture': []
                       }
            result = dict()
            result['status'] = 'success'
            result['token'] = token
            result['msg'] = ''
            result['data'] = company
        else:
            result = yield self.db.Company_company(company_id, token)

        self.write(ObjectToString().encode(result))
        self.finish()
        return

# 公司详情-所有职位get
class CompanyJobHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.asynchronous
    def post(self):
        self.log.info('+++++++++++Company all job+++++++++++')
        self.log.info(self.get_arguments())
        token = self.get_argument('token')
        page = self.get_argument('page')
        num = self.get_argument('num')
        job_type = self.get_argument('job_type')
        company_id = self.get_argument('company_id')
        company_name = self.get_argument('company_name')
        cache_flag = self.get_cache_flag()
        if company_id[:1] == '0':
            job = {'department': ['全部'],
                   'job': []}
            result = dict()
            result['status'] = 'success'
            result['token'] = token
            result['msg'] = ''
            result['data'] = job
        else:
            result = yield self.db.Company_job(company_id, company_name, token, page, num, job_type, cache_flag)

        self.write(ObjectToString().encode(result))
        self.finish()
        return
