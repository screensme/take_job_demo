#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import datetime
import time
import json
import requests,bcrypt
import configparser
from api.base_handler import BaseHandler
import logging
# import motor
import urllib, urllib2
import torndb
import tornado
from common.tools import args404, ObjectToString
import uuid
# from api import base_handler, company_handler, resume_handler, user_handler

class Action(object):
    def __init__(self, dbhost=str, dbname=str, dbuser=str, dbpwd=str, log=None, esapi=str):
        # pass
        self.db = torndb.Connection(host=dbhost,
                                    database=dbname,
                                    user=dbuser,
                                    password=dbpwd,
                                    )
        self.esapi = esapi
        self.log = log
        self.log.info('mysql=%s,db=%s' % (dbhost, dbname))
        print('init end')

    # 用户注册
    @tornado.gen.coroutine
    def Register_user(self, mobile=str, pwd=str, cache_flag=int):

        foo_uuid = str(uuid.uuid1())
        hash_pass = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

        user_info = self.db.get('SELECT * FROM rcat_test.candidate_user where phonenum=%s' % mobile)
        if user_info != None:
            result = dict()
            result['status'] = 'fail'
            result['msg'] = '手机号已经被注册'
            result['token'] = user_info['user_uuid']
            result['data'] = user_info
            raise tornado.gen.Return(result)
        else:
            try:
                user_info = self.db.get('SELECT * FROM rcat_test.candidate_user order by id DESC limit 1')
                _id = user_info['id'] + 1
                active = '1'
                authenticated = '1'
                post_status = 'allow'
                tag = 'test'
                dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # dd = dt_create.strftime("%Y-%m-%d %H:%M:%S")
                dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_write = self.db.insert(
                    "INSERT INTO rcat_test.candidate_user VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                _id, mobile, hash_pass, active, authenticated, post_status, tag, dt_create, dt_update, foo_uuid)

                result = dict()
                result['status'] = 'sucess'
                result['msg'] = ''
                result['token'] = foo_uuid
                result['data'] = {}
            except Exception, e:
                result = dict()
                result['status'] = 'fail'
                result['msg'] = e.log_message
                result['token'] = foo_uuid
                result['data'] = {}

        raise tornado.gen.Return(result)

    # 用户登陆
    @tornado.gen.coroutine
    def User_login(self, mobile=str,
                      pwd=str,
                      # umengid=str,
                      # mobibuild=str,
                      # mobitype=str,
                      cache_flag=int):
        result = dict()
        search_mobile = self.db.get("SELECT * FROM rcat_test.candidate_user WHERE phonenum=%s"
                                 % mobile)
        if search_mobile is None:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '没有此用户!'

        else:
            if search_mobile['password'] == bcrypt.hashpw(pwd.encode('utf-8'), search_mobile['password'].encode('utf-8')):
                sqll = "SELECT %s FROM candidate_cv as p left join candidate_user as q on q.id=p.user_id where q.id=%s" \
                       % ("id, user_id, username, sex, age, edu, school, major", search_mobile['id'])
                user_basic = self.db.get(sqll)
                if user_basic == None:
                    user_basic = {}
                result['status'] = 'success'
                result['msg'] = '登陆成功'
                result['token'] = search_mobile['id']
                result['data'] = user_basic
            else:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '密码错误!'
        raise tornado.gen.Return(result)

    # 用户登出
    @tornado.gen.coroutine
    def User_logout(self, token=str):
        # result = {}
        search_user = self.db.get("SELECT * FROM rcat_test.candidate_user WHERE id=%s"
                                 % token)
        result = dict()
        if (search_user['id'] != token):
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '没有此用户!'
                raise tornado.gen.Return(result)

        else:
            result['status'] = 'success'
            result['msg'] = '成功退出登录'
            result['token'] = token
            result['data'] = {}
        raise tornado.gen.Return(result)

    # 用户忘记密码
    # @tornado.gen.coroutine
    # def User_forgetpwd(mobile=str, pwd=str, cache_flag=int):
    #     pass
    #     result = dict()
    #     result['status'] = 'success'
    #     result['token'] = ''
    #     result['msg'] = ''
    #     result['data'] = {}
    #     # yield self.db["login_history"].insert({'mobile': mobile, 'pwd': pwd, 'act': 'login success'})
    #     raise tornado.gen.Return(result)

    # 用户修改密码
    @tornado.gen.coroutine
    def User_updatepwd(self, mobile=str, oldpwd=str, pwd=str, cache_flag=int):

        hash_oldpwd = bcrypt.hashpw(oldpwd.encode('utf-8'), bcrypt.gensalt())
        hash_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        sql = "SELECT * FROM rcat_test.candidate_user WHERE phonenum='%s'" % mobile
        search_user = self.db.get(sql)
        checkpw = isinstance(hash_oldpwd, search_user['password'])
        if search_user is None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '旧密码输入有误'
            result['data'] = {}
        else:
            update_pwd = self.db.update("UPDATE rcat_test.candidate_user set password=%s where mobile=%s",hash_pwd, mobile)

            result = dict()
            result['status'] = 'success'
            result['token'] = update_pwd['id']
            result['msg'] = '修改密码成功'
            result['data'] = {}
        raise tornado.gen.Return(result)

    # 个人信息页
    @tornado.gen.coroutine
    def Home_user(self, token=str, cache_flag=int):

        search_user = self.db.get("SELECT * FROM candidate_cv WHERE user_id='%s'" % token)
        try:
            search_us = json.loads(search_user['candidate_cv'])
        except Exception,e :
            pass
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_us
        raise tornado.gen.Return(result)

    # 首页
    @tornado.gen.coroutine
    def Home(self, token=str, cache_flag=int):

        uri = '%squery_new_job' % self.esapi
        values = dict()
        values['offset'] = 1
        values['limit'] = 10
        # values['query_new_job'] = '北京'
        reques = requests.post(url=uri, json=values)
        contect = reques.content.decode('utf-8')
        print contect
        contect_id = sorted(eval(contect)['id_list'])
        args = ','.join(str(x) for x in contect_id)
        search_job = self.db.query("SELECT %s FROM rcat_test.jobs_hot_es_test WHERE id IN (%s)"
                                 %('job_name,company_name,job_city,education_str,work_years_str,salary_str,boon,dt_update,scale_str,trade' ,args))

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_job
        raise tornado.gen.Return(result)

    # 首页搜索
    @tornado.gen.coroutine
    def Search_job(self, values=dict, token=str, cache_flag=int,):

        uri = '%squery_job' % self.esapi
        data = values.pop(u'token')
        values['offset'] = 1
        values['limit'] = 10
        reques = requests.post(url=uri, json=values)
        contect = reques.content.decode('utf-8')
        contect_id = sorted(eval(contect)['id_list'])
        args = ','.join(str(x) for x in contect_id)
        search_job = self.db.query("SELECT %s FROM rcat_test.jobs_hot_es_test WHERE id IN (%s)"
                                 %('job_name,company_name,job_city,education_str,work_years_str,salary_str,boon,dt_update,scale_str,trade' ,args))
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_job
        raise tornado.gen.Return(result)

    # 消息页，显示数量
    @tornado.gen.coroutine
    def Job_message(self, token=str, cache_flag=int):
        search_user = self.db.get("SELECT * FROM candidate_user WHERE id='%s'" % token)
        boss_profile = self.db.execute_rowcount("SELECT * FROM message WHERE receiver_user_id='%s' and status='unread'" % search_user['id'])

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = boss_profile
        raise tornado.gen.Return(result)

    # 简历状态查看get全部
    @tornado.gen.coroutine
    def Message_all(self, token=str,  cache_flag=int):

        # user_info = open('%s/message.txt'%filepath,'r+')
        # read_user = user_info.read().decode('gbk')
        # ev_user = eval(read_user)
        # print ev_user
        # user_info.close()
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str", token, 0, 2)
        try:
            boss_profile = self.db.query(sql)
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            boss_profile = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = boss_profile
        raise tornado.gen.Return(result)

    # 简历状态查看get被查看
    @tornado.gen.coroutine
    def Message_viewed(self, token=str, cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='viewed' limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, 0, 2)
        try:
            search_status = self.db.query(sql)
            if search_status == None:
                search_status = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            search_status = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        raise tornado.gen.Return(result)

    # 简历状态查看get已通知
    @tornado.gen.coroutine
    def Message_communicated(self, token=str, cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='notify' limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, 0, 2)
        try:
            search_status = self.db.query(sql)
            if search_status == None:
                search_status = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            search_status = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        raise tornado.gen.Return(result)

    # 简历状态查看get面试通过
    @tornado.gen.coroutine
    def Message_passed(self, token=str, cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status in ('pass', 'info') limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, 0, 2)
        try:
            search_status = self.db.query(sql)
            if search_status == None:
                search_status = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            search_status = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        raise tornado.gen.Return(result)

    # 简历状态查看get不合适
    @tornado.gen.coroutine
    def Message_improper(self, token=str, cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='deny' limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, 0, 2)
        try:
            search_status = self.db.query(sql)
            if search_status == None:
                search_status = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            search_status = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        raise tornado.gen.Return(result)

    # 职位详情
    @tornado.gen.coroutine
    def Position(self, job_id=str, token=str, cache_flag=int):

        search_job = self.db.get("select * from jobs_hot_es_test where id ='%s'" % job_id)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_job
        raise tornado.gen.Return(result)

    # 公司详情get
    @tornado.gen.coroutine
    def Company_full(self, company_id=str, token=str, cache_flag=int):

        sql = "select site_name,company_name from jobs_hot_es_test where id ='%s'" % company_id
        try:
            search_job = self.db.get(sql)
            if search_job['site_name'] == u'智联招聘':
                sqlll = "select * from spider_company where company_name ='%s'" % search_job['company_name']
                search_company = self.db.get(sqlll)
            else:
                sqll = "select * from company_detail where company_name ='%s'" % search_job['company_name']
                search_company = self.db.get(sqll)
            if search_company == None:
                search_company = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            search_company = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_company
        raise tornado.gen.Return(result)

    # 简历查看
    @tornado.gen.coroutine
    def Resume_view(self, token=str, cache_flag=int):

        search_resume = self.db.get("SELECT * FROM candidate_cv WHERE user_id=%s" % token)
        try:
            search_resume['candidate_cv'] = json.loads(search_resume['candidate_cv'])
        except Exception,e :
            pass

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_resume
        raise tornado.gen.Return(result)

    # 简历编辑-基本信息post
    @tornado.gen.coroutine
    def Resume_Basic(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-basic.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)

    # 简历编辑-教育经历post
    @tornado.gen.coroutine
    def Resume_Education(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-education.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)

    # 简历编辑-职业意向post
    @tornado.gen.coroutine
    def Resume_Expect(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-expect.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)

    # 简历编辑-实习经历post
    @tornado.gen.coroutine
    def Resume_Experience(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-experience.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)

    # 简历编辑-项目实践post
    @tornado.gen.coroutine
    def Resume_Item(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-item.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)

    # 简历编辑-自我评价post
    @tornado.gen.coroutine
    def Resume_Evaluation(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-evaluation.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)

    # 意见反馈
    @tornado.gen.coroutine
    def Feed_back(self, token=str, data=dict, cache_flag=int):

        user_info = open('%s/resume-feedback.txt'%filepath,'r+')
        ev_user = user_info.write(str(data))
        print data
        user_info.close()

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ev_user
        raise tornado.gen.Return(result)
