#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import datetime
import time
import json
import requests, bcrypt
from common.random_str import random_str
from api.base_handler import BaseHandler
import random
import redis
import torndb
import tornado
from common.tools import args404, ObjectToString
import uuid
from common.resume_default import cv_dict_default
from common.sms_api import SmsApi

class Action(object):
    def __init__(self, dbhost=str, dbname=str, dbuser=str, dbpwd=str, log=None, sms=int, esapi=str,
                 cahost=str, caport=str, capassword=str, caseldb=int):
        # pass
        self.db = torndb.Connection(host=dbhost,
                                    database=dbname,
                                    user=dbuser,
                                    password=dbpwd,
                                    )
        pool = redis.ConnectionPool(host=cahost, port=caport, db=caseldb, password=capassword)
        self.cacheredis = redis.StrictRedis(connection_pool=pool)
        self.esapi = esapi
        self.log = log
        self.sms = sms
        self.log.info('mysql=%s, db=%s, esapi=%s, cache=%s' % (dbhost, dbname, esapi, cahost))
        print('init end')

    # 用户注册
    @tornado.gen.coroutine
    def Register_user(self, mobile=str, pwd=str, code=str, cache_flag=int):

        result = dict()
        foo_uuid = str(uuid.uuid1())
        hash_pass = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

        user_info = self.db.get('SELECT * FROM rcat_test.candidate_user where phonenum=%s' % mobile)
        if user_info != None:
            result['status'] = 'fail'
            result['msg'] = '手机号已经被注册'
            result['token'] = user_info['id']
            result['data'] = {}
            raise tornado.gen.Return(result)
        else:
            # 验证手机验证码是否正确
            verify_code = self.cacheredis.get(mobile+"msgcode")
            if verify_code is None:
                result['status'] = 'fail'
                result['msg'] = '验证码超时，请重新获取'
                result['token'] = ''
                result['data'] = {'token': ''}
                raise tornado.gen.Return(result)

            elif verify_code != code:
                result['status'] = 'fail'
                result['msg'] = '验证码错误，请核对输入'
                result['token'] = ''
                result['data'] = {'token': ''}
                raise tornado.gen.Return(result)
            else:
                try:
                    # 添加用户
                    active = '1'
                    authenticated = '1'
                    post_status = 'allow'
                    tag = 'test'
                    dt_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dt_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sqll = "INSERT INTO rcat_test.candidate_user(phonenum, password, active, authenticated, post_status, tag, dt_create, dt_update, user_uuid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    user_write = self.db.insert(sqll,
                                                mobile, hash_pass, active, authenticated,
                                                post_status, tag, dt_created, dt_updated, foo_uuid)

                    result['status'] = 'sucess'
                    result['msg'] = ''
                    result['token'] = user_write
                    result['data'] = {'token': user_write}
                except Exception, e:
                    result['status'] = 'fail'
                    result['msg'] = e.message
                    result['token'] = ''
                    result['data'] = {'token': ''}

        raise tornado.gen.Return(result)

    # 用户登陆
    @tornado.gen.coroutine
    def User_login(self, mobile=str, pwd=str, cache_flag=int):
        result = dict()
        sql = "select id,password from candidate_user where phonenum=%s" % mobile
        search_mobile = self.db.get(sql)
        if search_mobile is None:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '没有此用户!'
                result['data'] = {}

        else:
            if search_mobile['password'] == bcrypt.hashpw(pwd.encode('utf-8'), search_mobile['password'].encode('utf-8')):
                # 查找用户基本信息(缺少用户头像，能不能数据库中加一个出来)
                sqll = "SELECT %s FROM candidate_cv  where user_id=%s" \
                       % ("username,sex,edu,school,major,candidate_cv", search_mobile['id'])
                user_basic = self.db.get(sqll)

                if user_basic is None:
                    user_basic = dict()
                    user_basic['id'] = str(search_mobile['id'])
                else:
                    candidate = json.loads(user_basic['candidate_cv'])
                    user_basic['id'] = str(search_mobile['id'])
                    user_basic['avatar'] = candidate['basic']['avatar']
                    user_basic.pop('candidate_cv')
                result['status'] = 'success'
                result['msg'] = '登陆成功'
                result['token'] = search_mobile['id']
                result['data'] = user_basic
            else:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '密码错误!'
                result['data'] = {}
        raise tornado.gen.Return(result)

    # 用户登出
    @tornado.gen.coroutine
    def User_logout(self, token=str):

        sql = "SELECT * FROM rcat_test.candidate_user WHERE id=%s" % token
        search_user = self.db.get(sql)
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

    # 忘记，找回密码
    @tornado.gen.coroutine
    def User_forgetpwd(self, mobile=str, pwd=str, code=str, cache_flag=int):

        result = dict()
        hash_pass = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        dt_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_search = "select * from candidate_user where phonenum=%s" % (mobile,)
        search_mobile = self.db.get(sql_search)
        if search_mobile == None:
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '该手机号未注册'
            result['data'] = {}
        else:
            # 验证手机验证码是否正确
            verify_code = self.cacheredis.get(mobile+"msgcode")
            if verify_code is None:
                result['status'] = 'fail'
                result['msg'] = '验证码超时，请重新获取'
                result['token'] = ''
                result['data'] = {'token': ''}
                raise tornado.gen.Return(result)

            elif verify_code != code:
                result['status'] = 'fail'
                result['msg'] = '验证码错误，请核对输入'
                result['token'] = ''
                result['data'] = {'token': ''}
                raise tornado.gen.Return(result)
            else:
                try:
                    sql_update = "update candidate_user set password=%s,dt_update=%s where phonenum=%s"
                    update_pwd = self.db.update(sql_update, hash_pass, dt_updated, mobile)
                    self.log.info('user update_pwd,id=%s' % update_pwd)
                    result['status'] = 'success'
                    result['token'] = search_mobile['id']
                    result['msg'] = ''
                    result['data'] = {}
                except Exception, e:
                    result['status'] = 'fail'
                    result['token'] = ''
                    result['msg'] = '服务器出错，请稍后'
                    result['data'] = {}
        raise tornado.gen.Return(result)

    # 用户修改密码
    @tornado.gen.coroutine
    def User_updatepwd(self, token=str, oldpwd=str, pwd=str, cache_flag=int):

        sql = "SELECT * FROM candidate_user WHERE id='%s'" % token
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
            update_pwd = self.db.update("update candidate_user set password=%s where id=%s", hash_pwd, token)

            self.log.info("user edit password %s (1 mean yes,0 nean no)")
            result = dict()
            result['status'] = 'success'
            result['token'] = search_user['id']
            result['msg'] = '修改密码成功'
            result['data'] = {}
        raise tornado.gen.Return(result)

    # 发送短信验证码post
    @tornado.gen.coroutine
    def Send_sms(self, mobile=str, key=str, cache_flag=int):

        random_number = random_str()
        result = dict()
        # sms == '0' 是真实发送
        if self.sms == 'yes':
            if key == "register":   # 注册
                ret_info = SmsApi().sms_register(mobile=mobile, rand_num=random_number)
                if ret_info['code'] == '0':
                    self.cacheredis.set(mobile+'msgcode', random_number, 5*60)
                    result['status'] = 'success'
                    result['token'] = ''
                    result['msg'] = '短信发送成功'
                    result['data'] = random_number
                else:
                    result['status'] = 'fail'
                    result['token'] = ''
                    result['msg'] = '短信发送失败'
                    result['data'] = {}
                raise tornado.gen.Return(result)
            elif key == "forgetpwd":    # 忘记密码
                ret_info = SmsApi().sms_forget(mobile=mobile, rand_num=random_number)
                if ret_info['code'] == '0':
                    self.cacheredis.set(mobile+'msgcode', random_number, 5*60)
                    result['status'] = 'success'
                    result['token'] = ''
                    result['msg'] = '短信发送成功'
                    result['data'] = random_number
                else:
                    result['status'] = 'fail'
                    result['token'] = ''
                    result['msg'] = '短信发送失败'
                    result['data'] = {}
                raise tornado.gen.Return(result)
        # sms == 'no' 不发送，验证码为1111111
        else:
            random_number = '111111'
            result = dict()

            self.cacheredis.set(mobile+'msgcode', random_number, 5*60)
            result['status'] = 'success'
            result['token'] = ''
            result['msg'] = '短信发送成功'
            result['data'] = random_number
            raise tornado.gen.Return(result)

    # 校验短信验证码get
    @tornado.gen.coroutine
    def Verification_sms(self, token=str, code=str, cache_flag=int):

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
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
        reques = requests.post(url=uri, json=values)
        contect = reques.content.decode('utf-8')
        self.log.info('id_list = %s' % contect)
        contect_id = sorted(eval(contect)['id_list'])
        args = ','.join(str(x) for x in contect_id)
        search_job = self.db.query("SELECT %s FROM rcat_test.jobs_hot_es_test WHERE id IN (%s)"
                                 %('id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_str,boon,dt_update,scale_str,trade' ,args))

        for index in search_job:
            index['company_logo'] = ''
            if index['job_type'] == 'fulltime':
                index['job_type'] = '全职'
            elif index['job_type'] == 'parttime':
                index['job_type'] = '兼职'
            elif index['job_type'] == 'intern':
                index['job_type'] = '实习'
            elif index['job_type'] == 'unclear':
                index['job_type'] = '不限'
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
        if 'job_type' in values:
            if 'fulltime' == values['job_type']:
                pass
            else:
                value['job_type'] = eval(value['job_type'])
        if 'education' in values:
            value['education'] = int(value['education'])
        # if 'work_years_start' in values:
        #     value['work_years_start'] = int(value['work_years_start'])
        # if 'work_years_end' in values:
        #     value['work_years_end'] = int(value['work_years_end'])
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
                if args != '':
                    search_job = self.db.query("SELECT %s FROM rcat_test.jobs_hot_es_test WHERE id IN (%s)"
                                             %('id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_str,boon,dt_update,scale_str,trade' ,args))
                    for index in search_job:
                        index['company_logo'] = ''
                        if index['job_type'] == 'fulltime':
                            index['job_type'] = '全职'
                        elif index['job_type'] == 'parttime':
                            index['job_type'] = '兼职'
                        elif index['job_type'] == 'intern':
                            index['job_type'] = '实习'
                        elif index['job_type'] == 'unclear':
                            index['job_type'] = '不限'
                else:
                    search_job = []
                result = dict()
                result['status'] = 'success'
                result['token'] = token
                result['msg'] = ''
                result['data'] = search_job
            except Exception, e:
                result = dict()
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = e
                result['data'] = {}
        raise tornado.gen.Return(result)

    # 热门搜索
    @tornado.gen.coroutine
    def Host_search_list(self, token=str, cache_flag=int):

        data = ['产品设计师', 'java', '测试工程师', '运营专员','运维工程师', '产品专员', '电商专员', 'PHP', 'C++', 'python']
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

        sql = "select * from view_user_collections where userid =%s and status='favorite' limit %s,%s"\
              % (token, page, num)
        try:
            search_status = self.db.query(sql)
            status = 'success'
            if search_status == None:
                search_status = {}
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            status = 'fail'
            search_status = {}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        raise tornado.gen.Return(result)

    # 收藏职位
    @tornado.gen.coroutine
    def user_add_collections(self, token=str, job_id=str, cache_flag=int):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = "select count(userid) from view_user_collections where userid =%s and jobid=%s " % (token, job_id)
        sql_ins = "INSERT INTO candidate_collection(user_id, job_id, status, dt_create, dt_update) VALUES (%s,%s,%s,%s,%s)"
        sql_up = "update candidate_collection set status=%s, dt_update=%s" \
                 " where user_id=%s and job_id=%s"

        try:
            # 查找是否收藏
            search_if = self.db.get(sql)
            if search_if['count(userid)'] == 0:
                result_sql = self.db.insert(sql_ins, token, job_id, 'favorite', dt, dt)
                result_sql['collect_id'] = result_sql
                msg = '已收藏'
            else:
                # 判断收藏状态（收藏或删除）
                sql_update = "select * from candidate_collection where user_id=%s and job_id=%s" % (token, job_id)
                search_status = self.db.get(sql_update)
                if search_status['status'] == "delete":
                    sta = 'favorite'
                    msg = '已收藏'
                    result_sql = self.db.update(sql_up, sta, dt, token, job_id)
                else:
                    sta = 'favorite'
                    msg = '已取消收藏'
                    result_sql = self.db.update(sql_up, sta, dt, token, job_id)
            status = 'success'
        except Exception, e:
            result_sql = self.log.info('ERROR is %s' % e)
            status = 'fail'
            msg = '收藏失败'
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = msg
        result['data'] = result_sql
        raise tornado.gen.Return(result)

    # 取消收藏职位(已不用)
    @tornado.gen.coroutine
    def user_cancel_collections(self, token=str, job_id=str, cache_flag=int):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = "update rcat_test.candidate_collection set status='delete', dt_update=%s" \
                 " where user_id=%s and job_id=%s"

        try:
            search_status = self.db.update(sql, dt, token, job_id)
            status = 'success'

        except Exception, e:
            search_status = self.log.info('ERROR is %s' % e)
            status = 'fail'
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = '成功取消收藏'
        result['data'] = search_status
        raise tornado.gen.Return(result)

    # 简历投递post
    @tornado.gen.coroutine
    def Post_resume(self, token=str, job_id=str, cache_flag=int):

        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "select * from candidate_post where user_id=%s and job_id=%s" % (token, job_id)

        try:
            search_status = self.db.get(sql)
            if search_status == None:
                match_rate = random.randint(50, 100)
                status = 'post'
                collect_status = ''
                sql_post = "insert into candidate_post(user_id, job_id, match_rate," \
                           " status, collect_status, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s)"
                post_resume = self.db.insert(sql_post, token, job_id, match_rate, status, collect_status, dt, dt)
                status = 'success'
                msg = '投递成功'
            else:
                status = 'fail'
                msg = '已投递的职位'
                post_resume = {}
            # 用户投递简历后，公司收到消息
            sql_company_userid = "select company_user_id from company_jd  where es_id =%s" % (job_id,)
            search_company_userid = self.db.get(sql_company_userid)
            if search_company_userid is None:
                status = 'fail'
                msg = '公司收消息错误'
            else:
                m_info = {'type': 'post',
                          'info': '您有新投递的简历'}
                sender = 'system'
                receiver_type = 'company',
                message_type = 'system',
                receiver_user_id = search_company_userid['company_user_id']
                message = json.dumps(m_info),
                sql_company = "insert into message(sender, receiver_type, message_type, receiver_user_id, message, status, dt_create, dt_update)" \
                              " values(%s,%s,%s,%s,%s,%s,%s,%s)"
                post_company = self.db.insert(sql_company, sender, receiver_type, message_type, receiver_user_id,
                                              message, 'unread', dt, dt)
                self.log.info('company receive user resume,message_id=%s' % post_company)
        except Exception, e:
            post_resume = self.log.info('ERROR is %s' % e)
            status = 'fail'
            msg = '服务器出错'
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = msg
        result['data'] = post_resume
        raise tornado.gen.Return(result)
