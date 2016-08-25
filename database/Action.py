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
from common.resume_default import cv_dict_default
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
            result['token'] = user_info['id']
            result['data'] = {}
            raise tornado.gen.Return(result)
        else:
            try:
                active = '1'
                authenticated = '1'
                post_status = 'allow'
                tag = 'test'
                dt_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # dd = dt_create.strftime("%Y-%m-%d %H:%M:%S")
                dt_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sqll = "INSERT INTO rcat_test.candidate_user(phonenum, password, active, authenticated, post_status, tag, dt_create, dt_update, user_uuid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                user_write = self.db.insert(sqll,
                                            mobile, hash_pass, active, authenticated,
                                            post_status, tag, dt_created, dt_updated, foo_uuid)

                result = dict()
                result['status'] = 'sucess'
                result['msg'] = ''
                result['token'] = user_write
                result['data'] = {'token': user_write}
            except Exception, e:
                result = dict()
                result['status'] = 'fail'
                result['msg'] = e.message
                result['token'] = ''
                result['data'] = {'token': ''}

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
        sql = "SELECT * FROM candidate_user WHERE phonenum=%s" % mobile
        search_mobile = self.db.get(sql)
        if search_mobile is None:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '没有此用户!'

        else:
            if search_mobile['password'] == bcrypt.hashpw(pwd.encode('utf-8'), search_mobile['password'].encode('utf-8')):
                sqll = "SELECT %s FROM candidate_cv as p left join candidate_user as q on q.id=p.user_id where q.id=%s" \
                       % ("user_id", search_mobile['id'])
                # user_id, username, sex, age, edu, school, major
                user_basic = self.db.get(sqll)
                if user_basic == None:
                    user_basic = {'id': str(search_mobile['id'])}
                else:
                    user_basic['id'] = str(search_mobile['id'])
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

        sql = "SELECT * FROM rcat_test.candidate_user WHERE phonenum='%s'" % mobile
        search_user = self.db.get(sql)
        if (search_user['password'] != bcrypt.hashpw(oldpwd.encode('utf-8'), search_user['password'].encode('utf-8'))) \
                or (search_user is None):
            result = dict()
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '旧密码输入有误'
            result['data'] = {}
        else:
            hash_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
            update_pwd = self.db.update("update candidate_user set password=%s where phonenum=%s", hash_pwd, mobile)

            self.log.info("user edit password %s (1 mean yes,0 nean no)")
            result = dict()
            result['status'] = 'success'
            result['token'] = search_user['id']
            result['msg'] = '修改密码成功'
            result['data'] = {}
        raise tornado.gen.Return(result)

    # 个人信息页
    @tornado.gen.coroutine
    def Home_user(self, token=str, cache_flag=int):

        sql = "SELECT %s FROM candidate_cv WHERE user_id='%s'" \
            % ("id, user_id, username, sex, age, edu, school, major", token)
        search_user = self.db.get(sql)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_user
        raise tornado.gen.Return(result)

    # 首页
    @tornado.gen.coroutine
    def Home(self, page=int, num=int, token=str, cache_flag=int):

        uri = '%squery_new_job' % self.esapi
        values = dict()
        values['offset'] = page
        values['limit'] = num
        # values['query_new_job'] = '北京'
        reques = requests.post(url=uri, json=values)
        contect = reques.content.decode('utf-8')
        print contect
        contect_id = sorted(eval(contect)['id_list'])
        args = ','.join(str(x) for x in contect_id)
        search_job = self.db.query("SELECT %s FROM rcat_test.jobs_hot_es_test WHERE id IN (%s)"
                                 %('id,job_name,company_name,job_city,education_str,work_years_str,salary_str,boon,dt_update,scale_str,trade' ,args))

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_job
        raise tornado.gen.Return(result)

    # 首页搜索
    @tornado.gen.coroutine
    def Search_job(self, values=dict, token=str, page=int, num=int, cache_flag=int,):

        uri = '%squery_job' % self.esapi
        a = values.pop('token')
        b = values.pop('page')
        c = values.pop('num')
        value = values
        if value == {}:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '请传入查找职位或公司'
            result['data'] = {}
        else:
            values['offset'] = page
            values['limit'] = num
            reques = requests.post(url=uri, json=values)
            contect = reques.content.decode('utf-8')
            try:
                contect_id = sorted(eval(contect)['id_list'])
                args = ','.join(str(x) for x in contect_id)
                search_job = self.db.query("SELECT %s FROM rcat_test.jobs_hot_es_test WHERE id IN (%s)"
                                         %('job_name,company_name,job_city,education_str,work_years_str,salary_str,boon,dt_update,scale_str,trade' ,args))
                result = dict()
                result['status'] = 'success'
                result['token'] = token
                result['msg'] = ''
                result['data'] = search_job
            except KeyError, e:
                result = dict()
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = '传入参数有误'
                result['data'] = {}
        raise tornado.gen.Return(result)

    # 热门搜索
    @tornado.gen.coroutine
    def Host_search_list(self, token=str, cache_flag=int,):

        data = ['测试工程师', '运维工程师', '产品专员', '产品设计师', '运营专员', '电商专员','java', 'PHP', 'C++', 'python']
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = data
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
    def Message_all(self, page=int, num=int, token=str,  cache_flag=int):

        # user_info = open('%s/message.txt'%filepath,'r+')
        # read_user = user_info.read().decode('gbk')
        # ev_user = eval(read_user)
        # print ev_user
        # user_info.close()
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, page, num)
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
    def Message_viewed(self, page=int, num=int, token=str,  cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='viewed' limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, page, num)
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
    def Message_communicated(self, page=int, num=int, token=str,  cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='notify' limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, page, num)
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
    def Message_passed(self, page=int, num=int, token=str,  cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status in ('pass', 'info') limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, page, num)
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
    def Message_improper(self, page=int, num=int, token=str,  cache_flag=int):

        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='deny' limit %s,%s"\
              % ("job_id,post_status,company_type,salary_str,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str",
                 token, page, num)
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
        if search_resume == None:
            search_resume = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_resume
        raise tornado.gen.Return(result)

    # 简历编辑-基本信息post
    @tornado.gen.coroutine
    def Resume_Basic(self, token=str, basic=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        # 新建
        if search_user is None:
            data = eval(basic)
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nowyear = datetime.datetime.now().strftime("%Y")
            age = int(nowyear) - int(data['birthday'])
            degree = ""
            school = ""
            major = ""
            data['avatar'] = ""
            cv_dict_default['basic'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            edit_resume = self.db.insert(sqll,
                                         int(token), data['name'], 'public', data['name'], data['gender'],
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(basic)
            data['avatar'] = basic_resume['basic']['avatar']
            basic_resume['basic'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '基本信息修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 简历编辑-教育经历post
    @tornado.gen.coroutine
    def Resume_Education(self, token=str, education=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        # 新建
        if search_user is None:
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            age = ""
            degree = ""
            school = ""
            major = ""
            data = eval(education)
            cv_dict_default['education'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            edit_resume = self.db.insert(sqll,
                                         int(token), "", 'public', "", "",
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(education)
            basic_resume['education'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '教育信息修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 简历编辑-职业意向post
    @tornado.gen.coroutine
    def Resume_Expect(self, token=str, expect=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        # 新建
        if search_user is None:
            data = eval(expect)
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            age = ""
            degree = ""
            school = ""
            major = ""
            cv_dict_default['intension'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            edit_resume = self.db.insert(sqll,
                                         int(token), "", 'public', "", "",
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
        # 修改
        else:
            expect_resume = json.loads(search_user['candidate_cv'])
            data = eval(expect)
            expect_resume['intension'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(expect_resume), dt, token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '职业意向修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 简历编辑-实习经历post
    @tornado.gen.coroutine
    def Resume_Career(self, token=str, career=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        # 新建
        if search_user is None:
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            age = ""
            degree = ""
            school = ""
            major = ""
            data = eval(career)
            cv_dict_default['career'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            edit_resume = self.db.insert(sqll,
                                         int(token), "", 'public', "", "",
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(career)
            basic_resume['career'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '实习经历修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 简历编辑-项目实践post
    @tornado.gen.coroutine
    def Resume_Item(self, token=str, data=dict, cache_flag=int):


        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '这个接口不用了'
        result['data'] = {}
        raise tornado.gen.Return(result)

    # 简历编辑-自我评价post
    @tornado.gen.coroutine
    def Resume_Evaluation(self, token=str, data=dict, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        # 新建--
        if search_user is None:
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            age = ""
            degree = ""
            school = ""
            major = ""
            cv_dict_default['extra'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            edit_resume = self.db.insert(sqll,
                                         int(token), "", 'public', "", "",
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
        # 修改
        else:
            expect_resume = json.loads(search_user['candidate_cv'])
            # data = basic_resume['basic']
            expect_resume['extra'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(expect_resume), dt, token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '自我评价修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 意见反馈
    @tornado.gen.coroutine
    def Feed_back(self, token=str, data=dict, cache_flag=int):


        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = {}
        raise tornado.gen.Return(result)

    # 查看收藏
    @tornado.gen.coroutine
    def view_user_collections(self, page=int, num=int, token=str, cache_flag=int):

        sql = "select * from view_user_collections where userid =%s  limit %s,%s" % (token, page, num)
        try:
            search_status = self.db.get(sql)
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

    # 收藏职位
    @tornado.gen.coroutine
    def user_add_collections(self, token=str, job_id=str, cache_flag=int):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = "select count(id) from view_user_collections where userid =%s and job_id=%s " % (token, job_id)
        sql_ins = "INSERT INTO rcat_test.candidate_collection " \
                  "VALUES (%s,%s,%s,%s,%s)" % (token, job_id, 'favorite', dt, dt)
        sql_up = "update candidate_collection set status='favorite', dt_update=%s" \
                 " where user_id=%s and job_id=%s" % (dt,token, job_id)

        try:
            result_sql = dict()
            search_status = self.db.query(sql)
            if search_status is 0:
                result_sql = self.db.insert(sql_ins)
            else:
                result_sql = self.db.update(sql_up)
                search_status = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            search_status = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = result_sql
        raise tornado.gen.Return(result)

    # 取消收藏职位
    @tornado.gen.coroutine
    def user_cancel_collections(self, token=str, job_id=str, cache_flag=int):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = "update rcat_test.candidate_collection set status='delete', dt_update=%s" \
                 " where user_id=%s and job_id=%s" % (dt, token, job_id)

        try:
            result_sql = dict()
            search_status = self.db.update(sql)

        except Exception, e:
            self.log.info('ERROR is %s' % e)
            search_status = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        raise tornado.gen.Return(result)
