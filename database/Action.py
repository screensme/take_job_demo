#!/usr/bin/env python
# encoding: utf-8
import sys
from tornado import gen
import datetime
import time
import json
import requests, bcrypt
from common.random_str import random_str
from copy import deepcopy
import random
import redis
import torndb
import tornado
import re
import uuid
from common.resume_default import cv_dict_default
from common.sms_api import SmsApi
from common import IF_email
from common.query_top import QueryEsapi
import oss2

reload(sys)
sys.setdefaultencoding("utf-8")

class Action(object):
    def __init__(self, dbhost=str, dbname=str, dbuser=str, dbpwd=str, log=None, sms=int, image=str, esapi=str,
                 cahost=str, caport=str, capassword=str, caseldb=int):
        # pass
        self.db = torndb.Connection(host=dbhost,
                                    database=dbname,
                                    user=dbuser,
                                    password=dbpwd,
                                    connect_timeout=5
                                    )
        pool = redis.ConnectionPool(host=cahost, port=caport, db=caseldb, password=capassword)
        self.cacheredis = redis.StrictRedis(connection_pool=pool)
        self.esapi = esapi
        self.log = log
        self.sms = sms
        self.image = image
        self.log.info('mysql=%s, db=%s, esapi=%s, cache=%s' % (dbhost, dbname, esapi, cahost))
        self.coonect = None
        print('init end')

    # 用户注册
    @tornado.gen.coroutine
    def Register_user(self, mobile=str, pwd=str, code=str, jiguang_id=str, umeng_id=str, cache_flag=int):

        result = dict()
        foo_uuid = str(uuid.uuid1())
        hash_pass = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

        user_info = self.db.get('SELECT * FROM candidate_user where phonenum=%s' % mobile)
        self.db.close()
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
                    tag = ''
                    user_name = ""
                    avatar = ""
                    sex = ""
                    dt_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dt_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sqll = "INSERT INTO candidate_user(phonenum, password, active, authenticated, post_status, tag, dt_create, dt_update, user_uuid, user_name, avatar, sex, jiguang_id, umeng_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.log.info("INSERT INTO candidate_user(phonenum, password, active, authenticated, post_status, tag, dt_create, dt_update, user_uuid, user_name, avatar, sex, jiguang_id, umeng_id) "
                                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (mobile, hash_pass, active, authenticated,
                                                                                    post_status, tag, dt_created, dt_updated, foo_uuid,
                                                                                    user_name, avatar, sex, jiguang_id, umeng_id))
                    user_write = self.db.insert(sqll,
                                                mobile, hash_pass, active, authenticated,
                                                post_status, tag, dt_created, dt_updated, foo_uuid,
                                                user_name, avatar, sex, jiguang_id, umeng_id)
                    self.db.close()

                    result['status'] = 'success'
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
    def User_login(self, mobile=str, pwd=str, jiguang_id=str, umeng_id=str,
                   app_version=str, mobile_version=str, mobile_type=str, cache_flag=int):
        result = dict()
        sql = "select id,password,user_name,sex,avatar,jiguang_id,umeng_id,proxy_user,mobile_type,mobile_version,app_version,job_id from candidate_user where phonenum=%s" % mobile
        try:
            search_mobile = self.db.get(sql)
        except Exception, e:
            self.log.info("-------------db error, reconnect, user login---------")
            self.db.reconnect()
            search_mobile = self.db.get(sql)
        self.db.close()
        if search_mobile is None:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '没有此用户!'
                result['data'] = {}
        else:
            if search_mobile['password'] == bcrypt.hashpw(pwd.encode('utf-8'), search_mobile['password'].encode('utf-8')):
                # 查询用户的简历一个字段,判断用户登录是否跳回简历填写页面
                sql_cv = "select candidate_cv from candidate_cv where user_id=%s" % search_mobile['id']
                try:
                    search_cv = self.db.get(sql_cv)
                    self.db.close()
                    self.log.info(search_cv)
                    if search_cv is None:
                        search_mobile['cv_name'] = ''
                    else:
                        # cv = json.loads(search_cv['candidate_cv'])
                        search_mobile['cv_name'] = "123456"
                except Exception, e:
                    result['status'] = 'fail'
                    result['token'] = ''
                    result['msg'] = '服务器错误，正在修复中!'
                    result['data'] = {}
                    raise tornado.gen.Return(result)
                if search_mobile['avatar'] != '':
                    search_mobile['avatar'] = "%s" % self.image + search_mobile['avatar']
                else:
                    pass

                if (jiguang_id != '') and (umeng_id != ''):
                    sql_umeng_jg = "update candidate_user set jiguang_id=%s,umeng_id=%s,job_id=%s where phonenum=%s"
                    self.db.update(sql_umeng_jg, jiguang_id, umeng_id, 0, mobile)
                    self.db.close()
                    search_mobile['jiguang_id'] = jiguang_id
                    search_mobile['umeng_id'] = umeng_id
                if (app_version != '') and (mobile_version != '') and (mobile_type != ''):
                    sql_app_mobile = "update candidate_user set app_version=%s,mobile_version=%s,mobile_type=%s,job_id=%s where phonenum=%s"
                    self.db.update(sql_app_mobile, app_version, mobile_version, mobile_type, 0, mobile)
                    self.db.close()
                    search_mobile['app_version'] = app_version
                    search_mobile['mobile_version'] = mobile_version
                    search_mobile['mobile_type'] = mobile_type
                # 修改所有为None的数据为""
                for ind in search_mobile:
                    if search_mobile[ind] == None:
                        search_mobile[ind] = ''
                search_mobile.pop('password')

                result['status'] = 'success'
                result['msg'] = '登陆成功'
                result['token'] = search_mobile['id']
                result['data'] = search_mobile

                sql_del = "update candidate_user set job_id=%s"
            else:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '密码错误!'
                result['data'] = {}

        raise tornado.gen.Return(result)

    # 用户登出
    @tornado.gen.coroutine
    def User_logout(self, token=str):

        sql = "SELECT * FROM candidate_user WHERE id=%s" % token
        search_user = self.db.get(sql)
        self.db.close()
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
        # hash_pass = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        # dt_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_search = "select * from candidate_user where phonenum=%s" % (mobile,)
        search_mobile = self.db.get(sql_search)
        self.db.close()
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
                    hash_pass = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
                    dt_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sql_update = "update candidate_user set password=%s,dt_update=%s where phonenum=%s"
                    update_pwd = self.db.update(sql_update, hash_pass, dt_updated, mobile)
                    self.db.close()
                    self.log.info('user update_pwd,id=%s' % update_pwd)
                    if search_mobile['avatar'] != '':
                        search_mobile['avatar'] = "%s" % self.image + search_mobile['avatar']
                    else:
                        pass
                    result['status'] = 'success'
                    result['token'] = search_mobile['id']
                    result['msg'] = ''
                    result['data'] = {'id': search_mobile['id'],
                                      'user_name': search_mobile['user_name'],
                                      'avatar': search_mobile['avatar'],
                                      'sex': search_mobile['sex'],
                                      }
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
        self.db.close()
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
            self.db.close()

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
                sql = "select id from candidate_user where phonenum=%s" % mobile
                search_mobile = self.db.get(sql)
                self.db.close()
                if search_mobile != None:
                    result['status'] = 'fail'
                    result['token'] = ''
                    result['msg'] = '手机号已经注册'
                    result['data'] = {}
                    raise tornado.gen.Return(result)
                ret_info = SmsApi().sms_register(mobile=mobile, rand_num=random_number)
                if ret_info['code'] != '500':
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
                if ret_info['code'] != '500':
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
        # sms == 'no' 不发送，验证码为111111
        else:
            random_number = '111111'
            result = dict()
            if key == "register":   # 注册
                sql = "select id from candidate_user where phonenum=%s" % mobile
                search_mobile = self.db.get(sql)
                self.db.close()
                if search_mobile != None:
                    result['status'] = 'fail'
                    result['token'] = ''
                    result['msg'] = '手机号已经注册'
                    result['data'] = {}
                    raise tornado.gen.Return(result)
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
        self.db.close()
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_user
        raise tornado.gen.Return(result)

    # 修改个人信息
    @tornado.gen.coroutine
    def User_info_edit(self, token=str, user_name=str, sex=str, avatar=str, cache_flag=int):

        result = dict()
        sql_update = "update candidate_user set user_name=%s,sex=%s where id=%s"
        try:
            search_user = self.db.update(sql_update, user_name, sex, token)
            self.db.close()
        except Exception, e:
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = e
            result['data'] = {}
            raise tornado.gen.Return(result)
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_user
        raise tornado.gen.Return(result)

    # 修改个人头像
    @tornado.gen.coroutine
    def User_avatar_edit(self, token=str, avatar=str, cache_flag=int):

        result = dict()
        sql_update = "update candidate_user set avatar=%s where id=%s"
        try:
            update_user = self.db.update(sql_update, avatar, token)
            self.db.close()
        except Exception, e:
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = e
            result['data'] = {}
            raise tornado.gen.Return(result)
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '修改个人头像成功'
        result['data'] = {}
        raise tornado.gen.Return(result)

    # 首页
    @tornado.gen.coroutine
    def Home_info(self, page=int, num=int, token=str, datas='', cache_flag=int):

        uri = '%squery_new_job' % self.esapi
        values = dict()
        if int(num) > 20:
            num = 20
        values['offset'] = int(page) * int(num)
        values['limit'] = int(num)
        if 'job_type' in datas:
            if 'fulltime' == datas['job_type']:
                pass
            else:
                values['job_type'] = eval(datas['job_type'])
        reques = requests.post(url=uri, json=values)
        contect = reques.content.decode('utf-8')
        try:
            contect_id = sorted(json.loads(contect)['id_list'])
            args = ','.join(str(x) for x in contect_id)
        except Exception, e:
            result = dict()
            result['status'] = 'success'
            result['token'] = token
            result['msg'] = '没有搜索结果'
            result['data'] = []
            raise tornado.gen.Return(result)

        sql_job = "SELECT id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num " \
                  "FROM jobs_hot_es_test WHERE id IN (%s) order by dt_update desc " % args

        search_job = self.db.query(sql_job)
        self.db.close()
        for index in search_job:
            # 调整所有为null的值为""
            for ind in index:
                if index[ind] == None:
                    index[ind] = ''
            # 薪资显示单位为K
            index['salary_start'] = index['salary_start'] / 1000
            if (index['salary_end'] % 1000) >= 1:
                index['salary_end'] = index['salary_end'] / 1000 + 1
            else:
                index['salary_end'] = index['salary_end'] / 1000
            if index['company_logo'] != '':
                index['company_logo'] = "%s" % self.image + index['company_logo']
            else:
                index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
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
    def Search_job(self, values=dict, cache_flag=int,):

        uri = '%squery_job' % self.esapi
        token = values.pop('token')
        page = values.pop('page')
        num = values.pop('num')
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
            if int(num) > 20:
                num = 20
            values['offset'] = int(page) * int(num)
            values['limit'] = num
            reques = requests.post(url=uri, json=values)
            contect = reques.content.decode('utf-8')
            try:
                contect_id = sorted(json.loads(contect)['id_list'])
                args = ','.join(str(x) for x in contect_id)
                if args != '':
                    search_job = self.db.query("SELECT %s FROM jobs_hot_es_test WHERE id IN (%s) order by dt_update desc"
                                             %('id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num' ,args))
                    self.db.close()
                    for index in search_job:
                        # 调整所有为null的值为""
                        for ind in index:
                            if index[ind] == None:
                                index[ind] = ''
                        # 薪资显示单位为K
                        if index['company_logo'] != '':
                            index['company_logo'] = "%s" % self.image + index['company_logo']
                        else:
                            index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                        index['salary_start'] = index['salary_start'] / 1000
                        if (index['salary_end'] % 1000) >= 1:
                            index['salary_end'] = index['salary_end'] / 1000 + 1
                        else:
                            index['salary_end'] = index['salary_end'] / 1000
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
                result['data'] = []
        raise tornado.gen.Return(result)

    # 公司搜索post
    @tornado.gen.coroutine
    def Search_company(self, values=dict, cache_flag=int,):

        uri = '%squery_company' % self.esapi
        token = values.pop('token')
        page = values.pop('page')
        num = values.pop('num')
        value = values
        if 'job_type' in values:
            if 'fulltime' == values['job_type']:
                pass
            else:
                value['job_type'] = eval(value['job_type'])
        if 'education' in values:
            value['education'] = int(value['education'])
        if value == {}:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '请传入查找的公司'
            result['data'] = {}
        else:
            if int(num) > 20:
                num = 20
            values['offset'] = int(page) * int(num)
            values['limit'] = num
            reques = requests.post(url=uri, json=values)
            contect = reques.content.decode('utf-8')
            try:
                contect_id = sorted(json.loads(contect)['id_list'])
                args = ','.join(str(x) for x in contect_id)
                if args != '':
                    search_job = self.db.query("SELECT %s FROM jobs_hot_es_test WHERE id IN (%s) order by dt_update desc"
                                             %('id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num' ,args))
                    self.db.close()
                    for index in search_job:
                        # 调整所有为null的值为""
                        for ind in index:
                            if index[ind] == None:
                                index[ind] = ''
                        # 薪资显示单位为K
                        if index['company_logo'] != '':
                            index['company_logo'] = "%s" % self.image + index['company_logo']
                        else:
                            index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                        index['salary_start'] = index['salary_start'] / 1000
                        if (index['salary_end'] % 1000) >= 1:
                            index['salary_end'] = index['salary_end'] / 1000 + 1
                        else:
                            index['salary_end'] = index['salary_end'] / 1000
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
                result['data'] = []
        raise tornado.gen.Return(result)

    # 职位推荐
    @tornado.gen.coroutine
    def Recommend_job(self, token=str, page=int, num=int, cache_flag=int,):
        # token = unlogin的时候，推荐什么；正常时候，用户信息为空时，推荐什么。

        if re.match(r'\d+', '%s' % token):      # 登陆状态
            uri = '%squery_recommend_job' % self.esapi
            sql_user_info = "select %s from candidate_cv where user_id=%s" % ('user_id,school,major,candidate_cv', token)
            search_user = self.db.get(sql_user_info)
            self.db.close()
        else:   # 未登录状态
            self.log.info('Recommend job, user==%s' % token)
            uri = '%squery_new_job' % self.esapi
            search_user = None
        values = dict()
        if search_user == None:     #
            uri = '%squery_new_job' % self.esapi
        else:
            candidate = json.loads(search_user['candidate_cv'])
            if candidate['intension']['title'] == "":
                pass
            else:
                values['job_name'] = candidate['intension']['title']
            if search_user['school'] == '':
                pass
            else:
                values['school_str'] = search_user['school']
            if search_user['major'] == '':
                pass
            else:
                values['major_str'] = search_user['major']
            if candidate['intension']['area'] == '':
                pass
            else:
                values['job_city'] = candidate['intension']['area']
        if int(num) > 20:
            num = 20
        values['offset'] = int(page) * int(num)
        values['limit'] = num
        reques = requests.post(url=uri, json=values)
        contect = reques.content.decode('utf-8')
        try:
            contect_id = sorted(json.loads(contect)['id_list'])
            if contect_id == []:
                uri = '%squery_new_job' % self.esapi
                val = dict()
                val['offset'] = int(page) * int(num)
                val['limit'] = num
                reques = requests.post(url=uri, json=val)
                contect = reques.content.decode('utf-8')
                contect_id = sorted(json.loads(contect)['id_list'])
            args = ','.join(str(x) for x in contect_id)
            if args != '':
                search_job = self.db.query("SELECT %s FROM jobs_hot_es_test WHERE id IN (%s)"
                                         %('id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num' ,args))
                self.db.close()
                for index in search_job:
                    for ind in index:
                        if index[ind] == None:
                            index[ind] = ""
                    if index['company_logo'] != '':
                        index['company_logo'] = "%s" % self.image + index['company_logo']
                    else:
                        index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                    index['salary_start'] = index['salary_start'] / 1000
                    if (index['salary_end'] % 1000) >= 1:
                        index['salary_end'] = index['salary_end'] / 1000 + 1
                    else:
                        index['salary_end'] = index['salary_end'] / 1000
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
            result['data'] = []
        raise tornado.gen.Return(result)

    # 急速招聘
    @tornado.gen.coroutine
    def Speed_job(self, value=dict, cache_flag=int,):

        uri = '%s/query_speed_jobs' % self.esapi
        token = value.pop('token')
        num = value.pop('num')
        page = value.pop('page')
        if int(num) > 20:
            num = 20
        if 'job_type' in value:
            if 'fulltime' == value['job_type']:
                pass
            else:
                value['job_type'] = eval(value['job_type'])
        value['offset'] = int(page) * int(num)
        value['limit'] = num
        reques = requests.post(url=uri, json=value)
        contect = reques.content.decode('utf-8')
        try:
            contect_id = sorted(json.loads(contect)['id_list'])
            args = ','.join(str(x) for x in contect_id)
            self.log.info(contect_id)
            if args != '':
                if re.match(r'\d+', '%s' % token):
                    is_proxy_user = "select proxy_user from candidate_user where id=%s" % token
                    search_proxy = self.db.get(is_proxy_user)
                    if search_proxy['proxy_user'] == 1:
                        select_type = 'j.id,j.job_name,j.job_type,j.company_name,j.job_city,j.education_str,j.work_years_str,j.salary_start,j.salary_end,j.boon,j.dt_update,j.scale_str,j.trade,j.company_logo,j.need_num,d.commission,d.commission_type'
                        query_sql = "SELECT %s FROM jobs_hot_es_test as j left join company_jd as d on j.id=d.es_id WHERE j.id IN (%s) order by dt_update desc"\
                                    % (select_type, args)
                        search_job = self.db.query(query_sql)
                    else:
                        select_type = 'id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num'
                        query_sql = "SELECT %s FROM jobs_hot_es_test WHERE id IN (%s)" % (select_type, args)
                        search_job = self.db.query(query_sql)
                    self.db.close()
                else:
                    select_type = 'id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num'
                    query_sql = "SELECT %s FROM jobs_hot_es_test WHERE id IN (%s)" % (select_type, args)
                    search_job = self.db.query(query_sql)
                    self.db.close()
                for n, index in enumerate(search_job):
                    # 调整所有为null的值为""
                    for ind in index:
                        if index[ind] == None:
                            index[ind] = ''
                    if index.has_key('commission'):
                        pass
                    else:
                        index['commission'] = 0
                    if index.has_key('commission_type'):
                        pass
                    else:
                        index['commission_type'] = '0'
                    # 添加图片
                    index['speed_image'] = "%s" % self.image + 'speed_job_%s.png' % n
                    # 公司logo
                    if index['company_logo'] != '':
                        index['company_logo'] = "%s" % self.image + index['company_logo']
                    else:
                        index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                    # 薪资显示单位为K
                    index['salary_start'] = index['salary_start'] / 1000
                    if (index['salary_end'] % 1000) >= 1:
                        index['salary_end'] = index['salary_end'] / 1000 + 1
                    else:
                        index['salary_end'] = index['salary_end'] / 1000
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
            result['data'] = []
        raise tornado.gen.Return(result)

    # 职为你来post
    @tornado.gen.coroutine
    def Job_For_Me(self, token=str, page=str, num=str, cache_flag=int,):

        uri = '%squery_priority_jobs' % self.esapi
        if int(num) > 20:
            num = 20
        value = dict()
        value['priority'] = 50
        value['offset'] = int(page) * int(num)
        value['limit'] = num
        reques = requests.post(url=uri, json=value)
        contect = reques.content.decode('utf-8')
        try:
            contect_id = sorted(json.loads(contect)['id_list'])
            args = ','.join(str(x) for x in contect_id)
            if args != '':
                search_job = self.db.query("SELECT %s FROM jobs_hot_es_test WHERE id IN (%s) order by dt_update desc"
                                         %('id,job_name,job_type,company_name,job_city,education_str,work_years_str,salary_start,salary_end,boon,dt_update,scale_str,trade,company_logo,need_num',args))
                self.db.close()
                for n, index in enumerate(search_job):
                    # 调整所有为null的值为""
                    for ind in index:
                        if index[ind] == None:
                            index[ind] = ''
                    # 添加图片
                    # index['speed_image'] = "%s" % self.image + 'speed_job_%s.png' % n
                    # 公司logo
                    if index['company_logo'] != '':
                        index['company_logo'] = "%s" % self.image + index['company_logo']
                    else:
                        index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                    # 薪资显示单位为K
                    index['salary_start'] = index['salary_start'] / 1000
                    if (index['salary_end'] % 1000) >= 1:
                        index['salary_end'] = index['salary_end'] / 1000 + 1
                    else:
                        index['salary_end'] = index['salary_end'] / 1000
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
            result['data'] = []
        raise tornado.gen.Return(result)

    # 热门搜索
    @tornado.gen.coroutine
    def Host_search_list(self, token=str, cache_flag=int):

        data = ['运营专员', 'java', '测试工程师','运维工程师','产品专员', '电商专员', '行政专员', 'C++', '文案策划']
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = data
        raise tornado.gen.Return(result)

    # 消息页，显示数量
    @tornado.gen.coroutine
    def Job_message(self, token=str, cache_flag=int):

        sql = "SELECT * FROM candidate_user WHERE id='%s'" % token
        search_user = self.db.get(sql)
        self.db.close()
        if search_user == None:
            boss_profile = 0
        else:
            sqll = "SELECT * FROM message WHERE receiver_user_id='%s' and status='unread'" % search_user['id']
            boss_profile = self.db.execute_rowcount(sqll)

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = boss_profile
        raise tornado.gen.Return(result)

    # 简历状态查看get全部
    @tornado.gen.coroutine
    def Message_all(self, page=int, num=int, token=str,  cache_flag=int):
        if int(num) > 20:
            num = 20
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id=p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s order by dt_update DESC limit %s offset %s"\
              % ("p.job_id,k.company_type,k.salary_start,k.salary_end,k.scale_str,k.job_city,k.company_name,k.boon,k.education_str,k.job_name,k.work_years_str,p.status,p.dt_update,k.company_logo",
                 token, num, (int(page) * int(num)))
        try:
            boss_profile = self.db.query(sql)
            self.db.close()
            for index in boss_profile:
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                for ind in index.keys():
                    if index[ind] == None:
                        index[ind] = ''
            status = 'success'
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            status = 'fail'
            boss_profile = {}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = boss_profile
        self.log.info(boss_profile)
        raise tornado.gen.Return(result)

    # 简历状态查看get被查看
    @tornado.gen.coroutine
    def Message_viewed(self, page=int, num=int, token=str,  cache_flag=int):
        if int(num) > 20:
            num = 20
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='viewed' order by dt_update DESC limit %s offset %s"\
              % ("p.job_id,k.company_type,k.salary_start,k.salary_end,k.scale_str,k.job_city,k.company_name,k.boon,k.education_str,k.job_name,k.work_years_str,p.status,p.dt_update,k.company_logo",
                 token, num, (int(page) * int(num)))
        try:
            search_status = self.db.query(sql)
            self.db.close()
            for index in search_status:
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                for ind in index.keys():
                    if index[ind] == None:
                        index[ind] = ''
            status = 'success'
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            status = 'fail'
            search_status = {}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        self.log.info(search_status)
        raise tornado.gen.Return(result)

    # 简历状态查看get简历通过
    @tornado.gen.coroutine
    def Message_communicated(self, page=int, num=int, token=str,  cache_flag=int):
        if int(num) > 20:
            num = 20
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status in ('pass', 'info') order by dt_update DESC limit %s offset %s"\
              % ("p.job_id,k.company_type,k.salary_start,k.salary_end,k.scale_str,k.job_city,k.company_name,k.boon,k.education_str,k.job_name,k.work_years_str,p.status,p.dt_update,k.company_logo",
                 token, num, (int(page) * int(num)))
        try:
            search_status = self.db.query(sql)
            self.db.close()
            for index in search_status:
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                for ind in index.keys():
                    if index[ind] == None:
                        index[ind] = ''
            status = 'success'
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            status = 'fail'
            search_status = {}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        self.log.info(search_status)
        raise tornado.gen.Return(result)

    # 简历状态查看get邀请面试
    @tornado.gen.coroutine
    def Message_passed(self, page=int, num=int, token=str,  cache_flag=int):
        if int(num) > 20:
            num = 20
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='notify' order by dt_update DESC limit %s offset %s"\
              % ("p.job_id,k.company_type,k.salary_start,k.salary_end,k.scale_str,k.job_city,k.company_name,k.boon,k.education_str,k.job_name,k.work_years_str,p.status,p.dt_update,k.company_logo",
                 token, num, (int(page) * int(num)))
        try:
            search_status = self.db.query(sql)
            self.db.close()
            for index in search_status:
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                for ind in index.keys():
                    if index[ind] == None:
                        index[ind] = ''
            status = 'success'
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            status = 'fail'
            search_status = {}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        self.log.info(search_status)
        raise tornado.gen.Return(result)

    # 简历状态查看get不合适
    @tornado.gen.coroutine
    def Message_improper(self, page=int, num=int, token=str,  cache_flag=int):
        if int(num) > 20:
            num = 20
        sql = "select %s from jobs_hot_es_test as k " \
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s and p.status='deny' order by dt_update DESC limit %s offset %s"\
              % ("p.job_id,k.company_type,k.salary_start,k.salary_end,k.scale_str,k.job_city,k.company_name,k.boon,k.education_str,k.job_name,k.work_years_str,p.status,p.dt_update,k.company_logo",
                 token, num, (int(page) * int(num)))
        try:
            search_status = self.db.query(sql)
            self.db.close()
            for index in search_status:
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                for ind in index.keys():
                    if index[ind] == None:
                        index[ind] = ''
            status = 'success'
        except Exception, e:
            self.log.info('ERROR is %s' % e[1])
            status = 'fail'
            search_status = {}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_status
        self.log.info(search_status)
        raise tornado.gen.Return(result)

    # 消息详情页，时间轴
    @tornado.gen.coroutine
    def Message_full(self, job_id=str, token=str,  cache_flag=int):

        sql = "select operate_massage from candidate_post where job_id=%s and user_id=%s" % (job_id, token)
        try:
            search_status = self.db.get(sql)
            self.db.close()
            if search_status is None:
                search_st = []
            else:
                if search_status['operate_massage'] is None:
                    search_st = []
                else:
                    search_st = json.loads(search_status['operate_massage'])
            status = 'success'
            self.log.info(search_st)
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            status = 'fail'
            search_st = []
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_st
        raise tornado.gen.Return(result)

    # 职位详情
    @tornado.gen.coroutine
    def Position_full(self, job_id=str, token=str, cache_flag=int):

        sql_job = "select %s from jobs_hot_es_test where id ='%s'"\
                  % ("site_name,salary_start,salary_end,job_name,job_city,job_type,boon,education_str,company_name,trade,company_type,scale_str,position_des,dt_update,company_logo,company_id,need_num",job_id)
        search_job = self.db.get(sql_job)
        self.db.close()
        if search_job == None:
            search_job = {}
        else:
            # 调整所有为null的值为""
            for index in search_job.keys():
                if search_job[index] == None:
                    search_job[index] = ''
            search_job['position_des'] = search_job['position_des'].replace("<br/>", "\n")
            if search_job['company_logo'] != '':
                search_job['company_logo'] = "%s" % self.image + search_job['company_logo']
            else:
                search_job['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
            search_job['boom'] = search_job.pop('boon')
            if search_job['job_type'] == 'fulltime':
                search_job['job_type'] = '全职'
            elif search_job['job_type'] == 'parttime':
                search_job['job_type'] = '兼职'
            elif search_job['job_type'] == 'intern':
                search_job['job_type'] = '实习'
            elif search_job['job_type'] == 'unclear':
                search_job['job_type'] = '不限'
            search_job['salary_start'] = search_job['salary_start'] / 1000
            if (search_job['salary_end'] % 1000) >= 1:
                search_job['salary_end'] = search_job['salary_end'] / 1000 + 1
            else:
                search_job['salary_end'] = search_job['salary_end'] / 1000
            if search_job['company_id'] == 0:
                search_job['company_address'] = ''
            else:
                try:
                    if search_job['site_name'] != 'local':
                        sql_address = "select address from spider_company where id ='%s'" % search_job['company_id']
                        search_company = self.db.get(sql_address)
                        self.db.close()
                        search_job['company_address'] = search_company['address']
                        search_job['company_id'] = str(search_job['company_id']) + '01'
                    else:
                        sql_address = "select company_address from company_detail where id ='%s'" % search_job['company_id']
                        search_company = self.db.get(sql_address)
                        self.db.close()
                        search_job['company_address'] = search_company['company_address']
                        search_job['company_id'] = str(search_job['company_id']) + '10'
                except Exception, e:
                    self.log.info("-------!!!!!!!!!!!!! Position_full, ERROR is %s" % e)
                    search_job['company_address'] = ''
                    # search_job['company_id'] = str(search_job['company_id']) + '01'
            try:
                if re.match(r'\d+', '%s' % token):      # 登陆
                    sql_collect = "select userid,jobid from view_user_collections where userid =%s and jobid=%s and status='favorite'" \
                                  % (token, job_id)
                    search_collect = self.db.query(sql_collect)
                    self.db.close()
                    sql_post = "select * from candidate_post where user_id=%s and job_id=%s" % (token, job_id)
                    search_post = self.db.query(sql_post)
                    self.db.close()
                    # 0-未收藏---未投递； 1-已收藏---已投递； 2-未登录
                    if search_collect == []:
                        search_job['collect'] = 0
                    else:
                        search_job['collect'] = 1
                    if search_post == []:
                        search_job['resume_post'] = 0
                    else:
                        search_job['resume_post'] = 1
                else:
                    search_job['collect'] = 2
                    search_job['resume_post'] = 2
            except Exception, e:
                self.log.info('============Position_full, ERROR is %s' % e)

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_job
        raise tornado.gen.Return(result)

    # 公司详情-公司信息get  01--spider 10-local
    @tornado.gen.coroutine
    def Company_basic(self, company_id=str, token=str, cache_flag=int):

        if company_id[-2:] == '01':
            sql_company = "select company_name,company_type,scale,address,company_trade,site_url,logo from spider_company where id='%s' limit 1" % company_id[:-2]
            search_company = self.db.get(sql_company)
            self.db.close()
            if search_company is None:
                company = {'company_name': '',
                           'company_trade': '',
                           'company_scale': '',
                           'company_type': '',
                           # 'company_address': '',
                           'company_site': '',
                           'company_logo': ''
                           }
            else:
                if search_company['logo'] != '':
                    logo = "%s" % self.image + search_company['logo']
                else:
                    logo = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)

                company = {'company_name': search_company['company_name'],
                           'company_trade': search_company['company_trade'],
                           'company_scale': search_company['scale'],
                           'company_type': search_company['company_type'],
                           # 'company_address': search_company['address'],
                           'company_site': search_company['site_url'],
                           'company_logo': logo
                           }
        elif company_id[-2:] == '10':
            sql_company = "select company_name,company_trade,company_scale,company_type,company_city,company_address,company_site,company_logo from company_detail where id='%s' limit 1" % company_id[:-2]
            search_company = self.db.get(sql_company)
            self.db.close()
            if search_company is None:
                company = {'company_name': '',
                           'company_trade': '',
                           'company_scale': '',
                           'company_type': '',
                           # 'company_address': '',
                           'company_site': '',
                           'company_logo': ''
                           }
            else:
                if search_company['company_logo'] != '':
                    logo = "%s" % self.image + search_company['company_logo']
                else:
                    logo = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                company = {'company_name': search_company['company_name'],
                           'company_trade': search_company['company_trade'],
                           'company_scale': search_company['company_scale'],
                           'company_type': search_company['company_type'],
                           # 'company_city': search_company['company_city'],
                           # 'company_address': search_company['company_address'] + search_company['company_city'],
                           'company_site': search_company['company_site'],
                           'company_logo': logo
                           }
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = 'company_id 有误'
            result['data'] = {}
            raise tornado.gen.Return(result)
        try:
            # 调整所有为null的值为""
            for index in company.keys():
                if company[index] == None:
                    company[index] = ''
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            company = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = company
        raise tornado.gen.Return(result)

    # 公司详情-企业详情get（公司介绍，大事记）    01--spider 10-local
    @tornado.gen.coroutine
    def Company_company(self, company_id=str, token=str, cache_flag=int):

        if company_id[-2:] == '01': # 爬虫公司
            sql_company = "select description,address from spider_company where id='%s' limit 1" % company_id[:-2]
            search_company = self.db.get(sql_company)
            self.db.close()
            if search_company is None:
                company = {'company_id': company_id,
                           'company_des': '',
                           'boon': '',
                           'events': '',
                           'company_address': '',
                           'picture': []
                           }
            else:
                company = {'company_id': company_id,
                           'company_des': search_company['description'],
                           'boon': '',
                           'events': '',
                           'company_address': search_company['address'],
                           'picture': []
                           }

        elif company_id[-2:] == '10':   # 真实公司
            sql_company = "select p.company_des,p.company_address,q.boon,q.events,GROUP_CONCAT(r.picture_name) from company_detail as p left join company_extra_info as q on p.company_user_id=q.company_user_id left join picture_attachment as r on p.company_user_id=r.company_user_id where p.id=%s limit 1" % company_id[:-2]
            self.log.info(sql_company)
            search_company = self.db.get(sql_company)
            self.db.close()
            if search_company is None:
                company = {'company_id': company_id,
                           'company_des': '',
                           'boon': '',
                           'events': '',
                           'company_address': '',
                           'picture': []
                           }
            else:
                if search_company['GROUP_CONCAT(r.picture_name)'] in ([], None):
                    pictures = []
                else:
                    pictures = search_company['GROUP_CONCAT(r.picture_name)'].split(',')
                    for p, q in enumerate(pictures):
                        # p = "%s" % self.image + p
                        pictures[p] = "%s" % self.image + q
                company = {'company_id': company_id,
                           'company_des': search_company['company_des'],
                           'boon': search_company['boon'],
                           'events': search_company['events'],
                           'company_address': search_company['company_address'],
                           'picture': pictures
                           }

        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = 'company_id 有误'
            result['data'] = {}
            raise tornado.gen.Return(result)
        try:
            # 调整所有为null的值为""
            for index in company.keys():
                if company[index] == None:
                    company[index] = ''
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            company = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = company
        raise tornado.gen.Return(result)

    # 公司详情-所有职位get  01--spider 10-local
    @tornado.gen.coroutine
    def Company_job(self, company_id=str, company_name=str, token=str, page=int, num=int, jobtype=str, cache_flag=int):
        if int(num) > 100:
            num = 100
        if company_id[-2:] == '01':
            uri = '%squery_company_jobs' % self.esapi
            values = dict()
            values['offset'] = int(page) * int(num)
            values['limit'] = num
            values['company_name'] = company_name
            reques = requests.post(url=uri, json=values)
            contect = reques.content.decode('utf-8')
            self.log.info('id_list = %s' % contect)
            contect_id = sorted(json.loads(contect)['id_list'])
            if contect_id == []:
                search_job = []
            else:
                args = ','.join(str(x) for x in contect_id)
                sql_job = "SELECT %s FROM jobs_hot_es_test WHERE id IN (%s) order by dt_update desc" \
                          %('id,job_name,job_type,job_city,education_str,salary_start,salary_end,dt_update,need_num',args)
                search_job = self.db.query(sql_job)
                self.db.close()
                for s in search_job:
                    s['job_id'] = s.pop('id')
                    s['department'] = ''
            department = ['全部']

        elif company_id[-2:] == '10':
            if jobtype != '全部':
                sql_job = "select a.job_name,a.es_id,a.department,a.education,a.job_type,a.salary_start,a.salary_end,a.job_city,a.need_num,a.dt_update from company_jd as a left join company_detail as b on a.company_user_id=b.company_user_id" \
                          " where b.id ='%s' and a.department='%s' order by dt_update desc limit %s offset %s" % (company_id[:-2], jobtype, num, (int(page) * int(num)))
            else:
                sql_job = "select a.job_name,a.es_id,a.department,a.education,a.job_type,a.salary_start,a.salary_end,a.job_city,a.need_num,a.dt_update from company_jd as a left join company_detail as b on a.company_user_id=b.company_user_id" \
                          " where b.id ='%s' order by dt_update desc limit %s offset %s" % (company_id[:-2], num, (int(page) * int(num)))

            search_job = self.db.query(sql_job)
            self.db.close()
            for x in search_job:
                x['job_id'] = x.pop('es_id')
                x['education_str'] = x.pop('education')
            sql_department = "select a.department from company_jd as a left join company_detail as b on a.company_user_id=b.company_user_id" \
                             " where b.id='%s'" % company_id[:-2]
            search_department = self.db.query(sql_department)
            self.db.close()
            department = ['全部']
            for x in search_department:
                if x['department'] not in department and x['department'] != '':
                    department.append(x['department'])

        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = 'company_id 有误'
            result['data'] = {}
            raise tornado.gen.Return(result)
        for index in search_job:
            # 调整所有为null的值为""
            for ind in index:
                if index[ind] == None:
                    index[ind] = ''
            # 薪资显示单位为K
            index['salary_start'] = index['salary_start'] / 1000
            if (index['salary_end'] % 1000) >= 1:
                index['salary_end'] = index['salary_end'] / 1000 + 1
            else:
                index['salary_end'] = index['salary_end'] / 1000
            if index['job_type'] == 'fulltime':
                index['job_type'] = '全职'
            elif index['job_type'] == 'parttime':
                index['job_type'] = '兼职'
            elif index['job_type'] == 'intern':
                index['job_type'] = '实习'
            elif index['job_type'] == 'unclear':
                index['job_type'] = '不限'

        job = {'department': department,
               'job': search_job}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = job
        raise tornado.gen.Return(result)

    # 500强公司链接
    @tornado.gen.coroutine
    def Job_500_Company(self, page=int, num=int, token=str, cache_flag=int):
        if int(num) > 30:
            num = 30

        sql = "select %s from job_500company where f_home>0 order by top_ranking limit %s offset %s" \
              % ("company_name,logo,logo_mobile,logo_mobile,url,f_home", num, (int(page) * int(num)))
        try:
            company_500 = self.db.query(sql)
            self.db.close()
        except Exception, e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '服务器错误'
            result['data'] = {'errorcode': 500}
            raise tornado.gen.Return(result)
        for index in company_500:
            index['logo'] = self.image + index['logo']
            if index['logo_mobile'] == None:
                index['logo_mobile'] = index['logo']

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = company_500
        raise tornado.gen.Return(result)

    # 简历查看
    @tornado.gen.coroutine
    def Resume_view(self, token=str, cache_flag=int):

        sql_resume = "SELECT id,user_id,openlevel,userclass,allow_post,dt_create,dt_update,candidate_cv FROM candidate_cv WHERE user_id=%s" % token
        search_resume = self.db.get(sql_resume)
        self.db.close()
        try:
            search_resume['candidate_cv'] = json.loads(search_resume['candidate_cv'])
            if search_resume['candidate_cv']['basic']['avatar'] != '':
                search_resume['candidate_cv']['basic']['avatar'] = "%s" % self.image + search_resume['candidate_cv']['basic']['avatar']
            else:
                pass
        except Exception, e:
            pass
        if search_resume == None:
            search_resume = {}
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_resume
        raise tornado.gen.Return(result)

    # 简历查看v1
    @tornado.gen.coroutine
    def Resume_V1_view(self, cv_id=str, token=str, cache_flag=int):

        if cv_id == 'Noneid':
            sql_resume = "SELECT id,user_id,openlevel,userclass,allow_post,dt_create,dt_update,candidate_cv FROM candidate_cv WHERE user_id=%s" % token
            search_resume = self.db.get(sql_resume)
            self.db.close()
            self.log.info("resume v1 -Noneid--- step 1")
        else:
            sql_resume = "SELECT id,user_id,openlevel,userclass,allow_post,dt_create,dt_update,candidate_cv FROM candidate_cv WHERE user_id=%s and id=%s" % (token, cv_id)
            search_resume = self.db.get(sql_resume)
            self.db.close()
            self.log.info("resume v1 -Haveid--- step 1+++")
        try:
            if search_resume is not None:
                search_resume['candidate_cv'] = json.loads(search_resume['candidate_cv'])
                if search_resume['candidate_cv']['basic']['avatar'] != '':
                    search_resume['candidate_cv']['basic']['avatar'] = "%s" % self.image + search_resume['candidate_cv']['basic']['avatar']
                else:
                    pass
                for uclass in search_resume['candidate_cv']['education']:
                    if 'classroom' not in uclass:
                        uclass['classroom'] = ''
                    else:
                        pass
                #     search_resume['userclass'] = ''
                try:
                    if cv_id == 'Noneid':
                        sql_certificate = "select id,certificate_name,certificate_image from candidate_cert where user_id=%s" % (token,)
                    else:
                        sql_certificate = "select id,certificate_name,certificate_image from candidate_cert where user_id=%s and cv_id=%s" % (token, cv_id)

                    search_cert = self.db.query(sql_certificate)
                    self.db.close()
                    self.log.info("resume v1 ---- step 2")

                    if search_cert is not None:
                        for i in search_cert:
                            i['certificate_image'] = self.image + i['certificate_image']
                        search_resume['candidate_cv']['certificate'] = search_cert
                    else:
                        search_resume['candidate_cv']['certificate'] = []
                    self.log.info("resume v1 ---- step 3")
                except KeyError, e:
                    self.log.info('----------- User candidate_cv certificate image fail')
                    pass
            else:
                search_resume = {}
                self.log.info('-------------- user is not have candidate_cv !!')
        except Exception, e:
            self.log.info('----------- Fail User candidate_cv certificate=%s' % e)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = search_resume
        raise tornado.gen.Return(result)

    # 简历编辑-修改头像post
    @tornado.gen.coroutine
    def Resume_Avatar(self, token=str, avatar=str, cache_flag=int):

        sql_resume = "SELECT id,candidate_cv FROM candidate_cv WHERE user_id=%s" % token
        search_resume = self.db.get(sql_resume)
        self.db.close()
        if search_resume == None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '此用户没有简历'
            result['data'] = {}
            raise tornado.gen.Return(result)
        else:
            sql_avatar = "update candidate_cv set candidate_cv=%s where user_id=%s"
            try:
                candidate_cv = json.loads(search_resume['candidate_cv'])
                candidate_cv['basic']['avatar'] = avatar
                candidate_json = json.dumps(candidate_cv)
                update_avatar = self.db.update(sql_avatar, candidate_json, token)
                self.log.info("update candidate_cv set candidate_cv=%s where user_id=%s" % (candidate_cv, token))

            except Exception, e:
                result = dict()
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = e
                result['data'] = {}
                raise tornado.gen.Return(result)

        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '修改简历头像成功'
        result['data'] = {}
        raise tornado.gen.Return(result)

    # 简历编辑-基本信息post
    @tornado.gen.coroutine
    def Resume_Basic(self, token=str, basic=str, userclass=str, cache_flag=int):
        self.log.info('+++++++++++Resume edit 2222222222+++++++++++')
        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        self.db.close()
        # 新建
        if search_user is None:
            self.log.info('==============Resume edit none 222222222==============')
            data = eval(basic)
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # nowyear = datetime.datetime.now().strftime("%Y")
            # age = int(nowyear) - int(data['birthday'])
            age = ""
            degree = ""
            school = ""
            major = ""
            data['avatar'] = ""
            cv_dict_default['basic'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username,userclass, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.log.info( "insert into candidate_cv(user_id, resume_name, openlevel, username,userclass, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                           %(token, data['name'], 'public', data['name'], userclass, data['gender'],
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update))
            edit_resume = self.db.insert(sqll,
                                         token, data['name'], 'public', data['name'], userclass, data['gender'],
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
            self.db.close()
            # 第一次新建的时候，流程跟网站相同。。然后将基本信息写到个人信息的数据库中
            sql_userinfo = "update candidate_user set user_name=%s,sex=%s where id=%s"
            self.log.info("update candidate_user set user_name=%s,sex=%s where id=%s" % (data['name'], data['gender'], token))
            insert_user_info = self.db.update(sql_userinfo, data['name'], data['gender'], token)
            self.db.close()
            self.log.info("user(%s) add resume-basic,resume_id=%s; AND update user_info" % (token, edit_resume, ))
        # 修改
        else:
            self.log.info('==============Resume edit yes 222222222==============')
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(basic)
            data['avatar'] = basic_resume['basic']['avatar']
            basic_resume['basic'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # nowyear = datetime.datetime.now().strftime("%Y")
            e_mail = basic_resume['basic']['email']
            if not IF_email.if_email(e_mail):
                result = dict()
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = '邮箱不合法'
                result['data'] = {'msg': 'email is not true'}
                raise tornado.gen.Return(result)

            resume_name = data['name'] + '的简历'
            username = data['name']
            sex = data['gender']
            high_edu = data['education']
            # age = int(nowyear) - int(data['birthday'])
            age = ""
            sqlll = 'update candidate_cv set resume_name=%s,username=%s,userclass=%s,sex=%s,age=%s,edu=%s,candidate_cv=%s,dt_update=%s where user_id=%s'
            self.log.info('update candidate_cv set resume_name=%s,username=%s,userclass=%s,sex=%s,age=%s,edu=%s,candidate_cv=%s,dt_update=%s where user_id=%s' % (resume_name, username, userclass, sex, age, high_edu, json.dumps(basic_resume), dt, token))
            edit_resume = self.db.update(sqlll, resume_name, username, userclass, sex, age, high_edu, json.dumps(basic_resume), dt, token)
            self.db.close()
            # 判断简历是否能投简历,1可以,0不可以
            J_post = self.Judgment_resume(token=token)
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
        self.log.info(sql)
        search_user = self.db.get(sql)
        self.db.close()

        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 新建
        if search_user is None:
            age = ""
            degree = ""
            school = ""
            major = ""
            userclass = ""
            data = eval(education)
            cv_dict_default['education'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username, userclass,sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.log.info("insert into candidate_cv(user_id, resume_name, openlevel, username,userclass, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                          % (token, "", 'public', "", userclass, "",
                             age, degree, school, major, json_cv,
                             dt, dt))
            edit_resume = self.db.insert(sqll,
                                         token, "", 'public', "", userclass, "",
                                         age, degree, school, major, json_cv,
                                         dt, dt)
            self.db.close()
        # 修改(传过来的数据至少有一条全都是空字符串的数据)
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(education)
            basic_resume['education'] = deepcopy(data)
            if data == []:
                sql_null = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
                edit_resume = self.db.update(sql_null, json.dumps(basic_resume), dt, token)
                self.db.close()
            else:
                if data[0]['end_time'] == '':
                    sqllll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
                    edit_resume = self.db.update(sqllll, json.dumps(basic_resume), dt, token)
                    self.db.close()
                else:
                    for item in data:
                        item['end_time'] = int(time.mktime(time.strptime(item['end_time'], "%Y.%m")))
                    data.sort(key=lambda x: x['end_time'], reverse=True)
                    one_edu = data[0]
                    school = one_edu['school']
                    major = one_edu['major']
                    edu = one_edu['degree']
                    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sqlll = 'update candidate_cv set edu=%s,school=%s,major=%s,candidate_cv=%s,dt_update=%s where user_id=%s'
                    edit_resume = self.db.update(sqlll, edu, school, major, json.dumps(basic_resume), dt, token)
                    self.db.close()
            # 判断简历是否能投简历,1可以,0不可以
            J_post = self.Judgment_resume(token=token)
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
        self.db.close()
        # 新建
        if search_user is None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '职业意向出错'
            result['data'] = {"errorcode": 1000}
            raise tornado.gen.Return(result)
        # 修改
        else:
            expect_resume = json.loads(search_user['candidate_cv'])
            data = eval(expect)
            expect_resume['intension'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(expect_resume), dt, token)
            self.db.close()

            # 判断简历是否能投简历,1可以,0不可以
            J_post = self.Judgment_resume(token=token)
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
        self.db.close()
        # 新建
        if search_user is None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '实习经历出错'
            result['data'] = {"errorcode": 1000}
            raise tornado.gen.Return(result)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(career)
            basic_resume['career'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
            self.db.close()

            # 判断简历是否能投简历,1可以,0不可以
            J_post = self.Judgment_resume(token=token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '实习经历修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 简历编辑-项目实践post(这个接口不用了)
    @tornado.gen.coroutine
    def Resume_experience(self, token=str, experience=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        self.db.close()
        # 新建
        if search_user is None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '项目实践出错'
            result['data'] = {"errorcode": 1000}
            raise tornado.gen.Return(result)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(experience)
            basic_resume['experience'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
            self.db.close()

            # # 判断简历是否能投简历,1可以,0不可以
            # J_post = self.Judgment_resume(token=token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '项目经历修改成功'
        result['data'] = {'errorcode': 0,}
        raise tornado.gen.Return(result)

    # 简历编辑-校内工作post(这个接口不用了)
    @tornado.gen.coroutine
    def Resume_Schooljob(self, token=str, school_job=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        self.db.close()
        # 新建
        if search_user is None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '校内工作出错'
            result['data'] = {"errorcode": 1000}
            raise tornado.gen.Return(result)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(school_job)
            basic_resume['school_job'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
            self.db.close()

            # # 判断简历是否能投简历,1可以,0不可以
            # J_post = self.Judgment_resume(token=token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '校内职位修改成功'
        result['data'] = {'errorcode': 0,}
        raise tornado.gen.Return(result)

    # 简历编辑-校内奖励post(这个接口不用了)
    @tornado.gen.coroutine
    def Resume_school_rewards(self, token=str, school_rewards=str, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        self.db.close()
        # 新建
        if search_user is None:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '职业意向出错'
            result['data'] = {"errorcode": 1000}
            raise tornado.gen.Return(result)
        # 修改
        else:
            basic_resume = json.loads(search_user['candidate_cv'])
            data = eval(school_rewards)
            basic_resume['school_rewards'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(basic_resume), dt, token)
            self.db.close()

            # # 判断简历是否能投简历,1可以,0不可以
            # J_post = self.Judgment_resume(token=token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '校内奖励修改成功'
        result['data'] = {'errorcode': 0,}
        raise tornado.gen.Return(result)

    # 简历新建-获得证书post
    @tornado.gen.coroutine
    def Resume_Certificate_addnew(self, token=str, cv_id=str, certificate_name=str, certificate_image=str, cache_flag=int):

        result = dict()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sqlll = 'insert into candidate_cert(user_id,cv_id,certificate_name,certificate_image,dt_create,dt_update) values(%s,%s,%s,%s,%s,%s)'
        try:
            edit_resume = self.db.insert(sqlll, token, cv_id, certificate_name, certificate_image, dt, dt)
            self.db.close()
        except Exception, e:
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '服务器错误'
            result['data'] = {'errorcode': 1000}
            raise tornado.gen.Return(result)

        # # 判断简历是否能投简历,1可以,0不可以
        # J_post = self.Judgment_resume(token=token)

        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '获得证书新建成功'
        result['data'] = {'errorcode': 0}
        raise tornado.gen.Return(result)

    # 简历编辑-获得证书put
    @tornado.gen.coroutine
    def Resume_Certificate(self, token=str, certificate_id=str, certificate_name=str, certificate_image=str, cache_flag=int):

        result = dict()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if certificate_image == '':
                sqlll = 'update candidate_cert set certificate_name=%s,dt_update=%s where id=%s and user_id=%s'
                edit_resume = self.db.update(sqlll, certificate_name, dt, certificate_id, token)
                self.db.close()
            else:
                sqlll = 'update candidate_cert set certificate_name=%s,certificate_image=%s,dt_update=%s where id=%s and user_id=%s'

                edit_resume = self.db.update(sqlll, certificate_name, certificate_image, dt, certificate_id, token)
                self.db.close()
        except Exception, e:
            self.log.info('-----!!!!!----%s' % e)
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '服务器错误'
            result['data'] = {'errorcode': 1000}
            raise tornado.gen.Return(result)

        # # 判断简历是否能投简历,1可以,0不可以
        # J_post = self.Judgment_resume(token=token)
        
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '获得证书修改成功'
        result['data'] = {'errorcode': 0}
        raise tornado.gen.Return(result)

    # 简历编辑-删除获得证书delete
    @tornado.gen.coroutine
    def Resume_Certificate_delete(self, token=str, certificate_id=str, cache_flag=int):

        result = dict()
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sqlll = 'delete from candidate_cert where id=%s and user_id=%s' % (certificate_id, token)
        try:
            edit_resume = self.db.execute(sqlll)
            self.db.close()
        except Exception, e:
            self.log.info('-----!!!!!----%s' % e)
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '服务器错误'
            result['data'] = {'errorcode': 1000}
            raise tornado.gen.Return(result)

        # # 判断简历是否能投简历,1可以,0不可以
        # J_post = self.Judgment_resume(token=token)
        
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '获得证书删除成功'
        result['data'] = {'errorcode': 0}
        raise tornado.gen.Return(result)

    # 简历编辑-自我评价post
    @tornado.gen.coroutine
    def Resume_Evaluation(self, token=str, data=dict, cache_flag=int):

        sql = "select * from candidate_cv where user_id=%s" % token
        search_user = self.db.get(sql)
        self.db.close()
        # 新建--
        if search_user is None:
            dt_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            age = ""
            degree = ""
            school = ""
            major = ""
            userclass = ""
            cv_dict_default['extra'] = data
            json_cv = json.dumps(cv_dict_default)
            sqll = "insert into candidate_cv(user_id, resume_name, openlevel, username,userclass, sex, age, edu, school, major, candidate_cv, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            edit_resume = self.db.insert(sqll,
                                         token, "", 'public', "", userclass, "",
                                         age, degree, school, major, json_cv,
                                         dt_create, dt_update)
            self.db.close()
        # 修改
        else:
            expect_resume = json.loads(search_user['candidate_cv'])
            # data = basic_resume['basic']
            expect_resume['extra'] = data
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlll = 'update candidate_cv set candidate_cv=%s,dt_update=%s where user_id=%s'
            edit_resume = self.db.update(sqlll, json.dumps(expect_resume), dt, token)
            self.db.close()
            # 判断简历是否能投简历,1可以,0不可以
            J_post = self.Judgment_resume(token=token)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '自我评价修改成功'
        result['data'] = edit_resume
        raise tornado.gen.Return(result)

    # 意见反馈
    @tornado.gen.coroutine
    def Feed_back(self, token=str, info=str, email=str, cache_flag=int):

        dt = datetime.datetime.now()
        job_type = "students"
        channel = "school"
        contents = info
        email = email
        status = "ready"
        sql_feed_post = "insert into feedback(job_type,channel,contents,status,dt_create,dt_update,email) values(%s,%s,%s,%s,%s,%s,%s)"
        try:
            feed_post = self.db.insert(sql_feed_post, job_type, channel, contents, status, dt, dt, email)
            self.db.close()
        except Exception, e:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '数据添加不成功'
            result['data'] = {'errorcode': 10}
            raise tornado.gen.Return(result)
        result = dict()
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = '反馈成功'
        result['data'] = {'errorcode': 0}
        raise tornado.gen.Return(result)

    # 获取版本,自动更新（仅Android）
    @tornado.gen.coroutine
    def Get_Version(self, Version=str, cache_flag=int):

        result = dict()
        version_get = Version.split('.')
        if len(version_get) != 3:
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '版本号格式有误'
            result['data'] = {'errorcode': 10,
                              'isupdate': 0,
                              'version': '',
                              'update_url': ''}
            raise tornado.gen.Return(result)
        else:
            sql_version = "select version,app_file from app_version where status!='delete' order by id desc limit 1 "
            try:
                version_post = self.db.get(sql_version)
                self.db.close()
                self.log.info('-------------------Search version end--')
                version_sql = version_post['version'].split('.')
                isupdate = 0
                for num in xrange(len(version_get)):
                    if version_get[num] < version_sql[num]:
                        isupdate = 1
                        break

            except Exception, e:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '数据添加不成功'
                result['data'] = {'errorcode': 10,
                                  'isupdate': 0,
                                  'version': '',
                                  'update_url': ''}
                raise tornado.gen.Return(result)
            result['status'] = 'success'
            result['token'] = ''
            result['msg'] = ''
            result['data'] = {'errorcode': 0,
                              'isupdate': isupdate,
                              'version': version_post['version'],
                              'update_url': self.image + version_post['app_file']
                              }
            raise tornado.gen.Return(result)

    # 申请成为校园代理post
    @tornado.gen.coroutine
    def Application_proxy_user(self, token=str, cache_flag=int):

        result = dict()
        sql_user = "select id,proxy_user from candidate_user where id=%s" % token
        search_user = self.db.get(sql_user)
        self.db.close()
        if search_user is None:
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '没有此用户'
            result['data'] = {'errorcode': 10,
                              }
        else:
            if search_user['proxy_user'] != 0:
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = '已经申请校园代理，请不要重复提交'
                result['data'] = {'errorcode': 20,
                                  }
            else:
                J_post = self.Judgment_resume(token=token)
                if J_post:
                    try:
                        tt = datetime.datetime.now()
                        sql_update = "update candidate_user set proxy_user=%s,dt_update=%s where id=%s"
                        update_user = self.db.update(sql_update, 2, tt, token)

                        self.log.info("update candidate_user set proxy_user=%s where id=%s" % (2, token))
                        result['status'] = 'success'
                        result['token'] = token
                        result['msg'] = '申请成功，我们会尽快联系您'
                        result['data'] = {'errorcode': 0,
                                          }
                    except Exception, e:
                        result['status'] = 'fail'
                        result['token'] = token
                        result['msg'] = e
                        result['data'] = {'errorcode': 1000,
                                          }
                else:
                    result['status'] = 'fail'
                    result['token'] = token
                    result['msg'] = '请将简历填写完整后申请成为合伙人'
                    result['data'] = {'errorcode': 50,
                                      }
        raise tornado.gen.Return(result)

    # # 职业导航
    # @tornado.gen.coroutine
    # def MajorList(self, major=str, token=str, cache_flag=int):
    #     result = dict()
    #
    #     user_code = None
    #     seo = None
    #     sql_seo = "select * from seo where seo_type=%s and seo_page=%s and isshow=%s"\
    #               % ('candidate', 'major_list', 'yes')
    #     try:
    #         seo = self.db.get(sql_seo)
    #         self.db.close()
    #     except Exception as e:
    #         self.log.info(e)
    #
    #     seo_cahe = self.cacheredis.get('candidate_major_list')
    #     if seo_cahe is None:
    #         seo_cahe = seo
    #         self.cacheredis.set('candidate_major_list', seo, ex=24*60*60)
    #
    #     sql_user = "select * from candidate_user where id=%s" % (token,)
    #     is_proxy_user = self.db.get(sql_user)
    #     self.db.close()
    #     if is_proxy_user is None:
    #         result = dict()
    #         result['status'] = 'fail'
    #         result['token'] = token
    #         result['msg'] = '用户不存在'
    #         result['data'] = {}
    #     else:
    #         if is_proxy_user['proxy_user'] != 1:
    #             sql_code = "select * from invite_user where user_id=%s" % (token,)
    #             try:
    #                 user_code = self.db.get(sql_code)
    #                 self.db.close()
    #             except Exception ,e:
    #                 result = {'major': '',
    #                           'major_list': [],
    #                           'major_first': [],
    #                           'major_second': [],
    #                           'head_list': [],
    #                           'hot_job_list_top': [],
    #                           'code': 0,
    #                           'order_code': '/invitecode',
    #                           'seo': seo,
    #                           }
    #                 raise tornado.gen.Return(result)
    #
    #     major_list_file = 'RcatAPP/helpers/major_list.json'
    #     major_list = self.cacheredis.get('major_list')
    #     if major_list is None:
    #         with open(major_list_file) as f:
    #             major_list = json.load(f)
    #             self.cacheredis.set('major_list', major_list, ex=24 * 60 * 60)
    #
    #     major_map_file = 'RcatAPP/helpers/major_map.json'
    #
    #     major_map = self.cacheredis.get('major_map')
    #     if major_map is None:
    #         with open(major_map_file) as f:
    #             major_map = json.load(f)
    #             self.cacheredis.set('major_map', major_map, ex=24 * 60 * 60)
    #
    #     # 判断缓存中是否有数据
    #     major_top_dict = self.cacheredis.get('{major}_job_top_dict'.format(major=major))
    #
    #     if major_top_dict is None:
    #         # 请求数据
    #         job_list = major_map.get(major, None)
    #         if job_list is not None:
    #
    #             try:
    #                 total = len(job_list)
    #                 sep_num = total - total // 3
    #                 job_first_list = job_list[:sep_num]
    #                 job_second_list = job_list[sep_num:]
    #
    #                 major_first_list = cs_api.query_multi_job_top(*job_first_list)
    #                 major_second_list = cs_api.query_multi_job_top(*job_second_list)
    #                 major_top_dict = {
    #                     'first': major_first_list,
    #                     'second': major_second_list
    #                 }
    #                 cache.set('{major}_job_top_dict'.format(major=major), major_top_dict, timeout=24 * 60 * 60)
    #             except Exception as e:
    #                 logger.exception(e)
    #                 major_top_dict = {
    #                     'first': [],
    #                     'second': [],
    #                 }
    #         else:
    #             major_top_dict = {
    #                 'first': [],
    #                 'second': [],
    #             }
    #
    #     trade = request.args.get('trade', '不限').strip()
    #     work_years = request.args.get('work_years', '应届').strip()
    #     payload = {
    #
    #         'trade': trade,
    #         'work_years': work_years,
    #     }
    #     data_list = cache.get(trade + work_years)
    #     if data_list is None:
    #         data_list = cs_api.query_trade_top(**payload)
    #         cache.set(trade + work_years, data_list, timeout=12 * 60 * 60)
    #
    #     # hot job_list
    #     hot_job_list = ['产品经理', 'HRBP', 'UI', '运营专员', '市场策划', '律师助理',
    #                     '行政管理', '会计', '人力资源专员', '招聘专员']
    #
    #     hot_job_list_top = cache.get('hot_job_list_top')
    #     if hot_job_list_top is None:
    #         hot_job_list_top = cs_api.query_multi_job_top(*hot_job_list)
    #         hot_job_list_top.sort(key=lambda x: hot_job_list.index(x['job_name']))
    #         cache.set('hot_job_list_top', hot_job_list_top, timeout=24 * 7 * 60 * 60)
    #
    #     ret = {
    #         'major': major,
    #         'major_list': major_list,
    #         'major_first': major_top_dict['first'],
    #         'major_second': major_top_dict['second'],
    #         'head_list': data_list,
    #         'hot_job_list_top': hot_job_list_top,
    #         'code': 1,
    #         'order_code': '',
    #         'seo': seo,
    #     }
    #     if user_agent.is_mobile or 'MicroMessenger' in ua_string:
    #         return abort(404)
    #     return render_template('candidate_tpl/major_list.html', **ret)

    # 职业导航首页
    @tornado.gen.coroutine
    def pro_navigation_list(self, invite_code=str, token=str, cache_flag=int):

        result = dict()
        if invite_code == '':
            sql_user = "select * from invite_user where user_id=%s" % (token,)
            search_user = self.db.get(sql_user)
            self.db.close()
            if search_user is None:
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = '请输入邀请码'
                result['data'] = {'errorcode': 10}
                raise tornado.gen.Return(result)

        else:
            sql_invite = "select * from invite_code where code='%s' and status='%s'" % (invite_code, 'unuse')
            search_invite = self.db.get(sql_invite)
            self.db.close()
            if search_invite is None:
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = '邀请码错误，请重新输入'
                result['data'] = {'errorcode': 20}
                raise tornado.gen.Return(result)
            else:
                dt = datetime.datetime.now()
                sql_update_invite_code = "update invite_code set status=%s,dt_update=%s where code=%s"
                update_invite = self.db.update(sql_update_invite_code, 'use', dt, invite_code)
                self.db.close()
                self.log.info('----------------------invite_code to invite_code!!! user=%s, code=%s' % (token, invite_code,))

                sql_insert_invite = "insert into invite_user(user_id, code_id, dt_create, dt_update) values(%s,%s,%s,%s)"
                insert_invite = self.db.insert(sql_insert_invite, token, search_invite['id'], dt, dt)
                self.db.close()
                self.log.info('----------------------invite_code to invite_user!!! user=%s, code=%s' % (token, invite_code,))

        ret = {'errorcode': 10,
               'major_list': [{'major_name': 'highsalary'},
                              {'major_name': 'hotjob'}],
               'trade_list': [{'id': 1, 'trade_name': '金融/银行/证券'},
                              {'id': 2, 'trade_name': '通信/电子'},
                              {'id': 3, 'trade_name': '市场/销售/客服'},
                              {'id': 4, 'trade_name': '房地产/建筑'},
                              {'id': 5, 'trade_name': '人力/行政/后勤'},
                              {'id': 6, 'trade_name': '设计/广告/媒体/艺术'}
                              ]
            }
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ret
        raise tornado.gen.Return(result)

    # 高薪职位排行榜
    @tornado.gen.coroutine
    def Rank_high_salary(self, token=str, cache_flag=int):

        result = dict()
        trade = '不限'
        work_years = '应届'
        try:
            if cache_flag:
                data_list = self.cacheredis.get('flask_cache_{trade}_{work_years}_headline'.format(trade=trade, work_years=work_years))
                if data_list is None:
                    data_list = QueryEsapi.query_trade_top(self.esapi)
                    self.cacheredis.set('flask_cache_{trade}_{work_years}_headline'.format(trade=trade, work_years=work_years), data_list, ex=24 * 7 * 60 * 60)
                else:
                    data_list = eval(data_list)
            else:
                data_list = QueryEsapi.query_trade_top(self.esapi)
                self.cacheredis.set('flask_cache_{trade}_{work_years}_headline'.format(trade=trade, work_years=work_years), data_list, ex=24 * 7 * 60 * 60)
        except Exception, e:
            self.log.info('--------------query_trade_top error !-----')
            data_list = []
        if data_list != []:
            for data in data_list:
                data['salary_avg'] = data['salary_avg'] + '元/月'
        # ret = [{'job_name': '置业顾问', 'salary_avg': '13,981'}, {'job_name': '数据分析', 'salary_avg': '7,931'}, {'job_name': '交易员', 'salary_avg': '7,828'}, {'job_name': '理财经理', 'salary_avg': '7,293'}, {'job_name': '投资顾问', 'salary_avg': '7,293'}, {'job_name': '培训师', 'salary_avg': '7,261'}, {'job_name': '招生顾问', 'salary_avg': '7,107'}, {'job_name': 'PHP', 'salary_avg': '7,080'}, {'job_name': 'java', 'salary_avg': '6,926'}, {'job_name': '教师', 'salary_avg': '6,882'}, {'job_name': '销售代表', 'salary_avg': '6,823'}, {'job_name': '软件工程师', 'salary_avg': '6,797'}, {'job_name': '电话销售', 'salary_avg': '6,630'}, {'job_name': '学术推广', 'salary_avg': '6,542'}, {'job_name': '市场专员', 'salary_avg': '6,542'}, {'job_name': '演员', 'salary_avg': '6,429'}, {'job_name': '艺人经纪人', 'salary_avg': '6,429'}, {'job_name': '美容顾问', 'salary_avg': '6,231'}, {'job_name': '化妆师', 'salary_avg': '6,231'}, {'job_name': '美容师', 'salary_avg': '6,231'}, {'job_name': '测试工程师', 'salary_avg': '5,863'}, {'job_name': '运营专员', 'salary_avg': '5,805'}, {'job_name': '会计', 'salary_avg': '5,636'}, {'job_name': '商务专员', 'salary_avg': '5,352'}, {'job_name': '招商专员', 'salary_avg': '5,352'}, {'job_name': 'UI', 'salary_avg': '5,309'}, {'job_name': '办公室文员', 'salary_avg': '5,111'}, {'job_name': '秘书', 'salary_avg': '4,857'}, {'job_name': '客服专员', 'salary_avg': '4,715'}, {'job_name': '招聘专员', 'salary_avg': '4,658'}, {'job_name': '市场策划', 'salary_avg': '4,588'}, {'job_name': '用户运营', 'salary_avg': '4,559'}, {'job_name': '行政管理', 'salary_avg': '4,559'}, {'job_name': '人力资源专员', 'salary_avg': '4,446'}, {'job_name': '内容编辑', 'salary_avg': '4,446'}, {'job_name': '编辑', 'salary_avg': '4,219'}, {'job_name': '产品设计师', 'salary_avg': '4,148'}, {'job_name': '会务专员', 'salary_avg': '4,120'}, {'job_name': '出纳', 'salary_avg': '3,680'}]

        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = data_list
        raise tornado.gen.Return(result)

    # 热门职位排行榜
    @tornado.gen.coroutine
    def rank_hot_job(self, token=str, cache_flag=int):

        result = dict()
        hot_job_list = ['产品经理', 'HRBP', 'UI', '运营专员', '市场策划', '律师助理',
                        '行政管理', '会计', '人力资源专员', '招聘专员']
        try:
            if cache_flag:
                hot_job_list_top = self.cacheredis.get('hot_job_list_top')
                if hot_job_list_top is None:
                    hot_job_list_top = QueryEsapi.query_multi_job_top(self.esapi, *hot_job_list)
                    hot_job_list_top.sort(key=lambda x: hot_job_list.index(x['job_name']))
                    self.cacheredis.set('hot_job_list_top', hot_job_list_top, ex=24 * 7 * 60 * 60)
                else:
                    hot_job_list_top = eval(hot_job_list_top)
                    # hot_job_list_top = json.loads(hot_job_list_top)
            else:
                hot_job_list_top = QueryEsapi.query_multi_job_top(self.esapi, *hot_job_list)
                hot_job_list_top.sort(key=lambda x: hot_job_list.index(x['job_name']))
                self.cacheredis.set('hot_job_list_top', hot_job_list_top, ex=24 * 7 * 60 * 60)
        except Exception, e:
            self.log.info('-------------- rank_hot_job error !-----')
            hot_job_list_top = []
        if hot_job_list_top != []:
            for data in hot_job_list_top:
                data['salary_avg'] = str(data['salary_avg']) + '元/月'

        # ret = [{'job_name': 'UI', 'salary_avg': 4827}, {'job_name': '运营专员', 'salary_avg': 5278}, {'job_name': '市场策划', 'salary_avg': 4171}, {'job_name': '行政管理', 'salary_avg': 4145}, {'job_name': '会计', 'salary_avg': 5124}, {'job_name': '人力资源专员', 'salary_avg': 4042}, {'job_name': '招聘专员', 'salary_avg': 4235}]
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = hot_job_list_top
        raise tornado.gen.Return(result)

    # 行业职位排行榜
    @tornado.gen.coroutine
    def rank_trade(self, trade=str, token=str, cache_flag=int):

        result = dict()
        if cache_flag:
            cache_job_list = None
            # cache_job_list = self.cacheredis.get('{trade}_job_list'.format(trade=trade))
            if cache_job_list is None:
                job_list = QueryEsapi.query_trade_top(self.esapi, trade)
                cache_job_list = self.cacheredis.set('{trade}_job_list'.format(trade=trade), job_list, ex=24 * 60 * 60)
            else:
                job_list = eval(cache_job_list)
        else:
            job_list = QueryEsapi.query_trade_top(self.esapi, trade)
            cache_job_list = self.cacheredis.set('{trade}_job_list'.format(trade=trade), job_list, ex=24 * 60 * 60)

        if job_list != []:
            for data in job_list:
                data['salary_avg'] = data['salary_avg'] + '元/月'
        # ret = [{'job_name': '置业顾问', 'salary_avg': '13,981'}, {'job_name': '数据分析', 'salary_avg': '7,931'}, {'job_name': '交易员', 'salary_avg': '7,828'}, {'job_name': '理财经理', 'salary_avg': '7,293'}, {'job_name': '投资顾问', 'salary_avg': '7,293'}, {'job_name': '培训师', 'salary_avg': '7,261'}, {'job_name': '招生顾问', 'salary_avg': '7,107'}, {'job_name': 'PHP', 'salary_avg': '7,080'}, {'job_name': 'java', 'salary_avg': '6,926'}, {'job_name': '教师', 'salary_avg': '6,882'}, {'job_name': '销售代表', 'salary_avg': '6,823'}, {'job_name': '软件工程师', 'salary_avg': '6,797'}, {'job_name': '电话销售', 'salary_avg': '6,630'}, {'job_name': '学术推广', 'salary_avg': '6,542'}, {'job_name': '市场专员', 'salary_avg': '6,542'}, {'job_name': '演员', 'salary_avg': '6,429'}, {'job_name': '艺人经纪人', 'salary_avg': '6,429'}, {'job_name': '美容顾问', 'salary_avg': '6,231'}, {'job_name': '化妆师', 'salary_avg': '6,231'}, {'job_name': '美容师', 'salary_avg': '6,231'}, {'job_name': '测试工程师', 'salary_avg': '5,863'}, {'job_name': '运营专员', 'salary_avg': '5,805'}, {'job_name': '会计', 'salary_avg': '5,636'}, {'job_name': '商务专员', 'salary_avg': '5,352'}, {'job_name': '招商专员', 'salary_avg': '5,352'}, {'job_name': 'UI', 'salary_avg': '5,309'}, {'job_name': '办公室文员', 'salary_avg': '5,111'}, {'job_name': '秘书', 'salary_avg': '4,857'}, {'job_name': '客服专员', 'salary_avg': '4,715'}, {'job_name': '招聘专员', 'salary_avg': '4,658'}, {'job_name': '市场策划', 'salary_avg': '4,588'}, {'job_name': '用户运营', 'salary_avg': '4,559'}, {'job_name': '行政管理', 'salary_avg': '4,559'}, {'job_name': '人力资源专员', 'salary_avg': '4,446'}, {'job_name': '内容编辑', 'salary_avg': '4,446'}, {'job_name': '编辑', 'salary_avg': '4,219'}, {'job_name': '产品设计师', 'salary_avg': '4,148'}, {'job_name': '会务专员', 'salary_avg': '4,120'}, {'job_name': '出纳', 'salary_avg': '3,680'}]
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = job_list
        raise tornado.gen.Return(result)

    # 工资走势图
    @tornado.gen.coroutine
    def salary_trend_list(self, job=str, token=str, cache_flag=int):

        result = dict()
        ret = {
            'search': job,
'salary_trend_list': [{'legend': '2015年11月', 'value': 16174}, {'legend': '2015年12月', 'value': 15513}, {'legend': '2016年1月', 'value': 15426}, {'legend': '2016年2月', 'value': 15808}, {'legend': '2016年3月', 'value': 16636}, {'legend': '2016年4月', 'value': 16358}, {'legend': '2016年5月', 'value': 15890}, {'legend': '2016年6月', 'value': 15973}, {'legend': '2016年7月', 'value': 16443}, {'legend': '2016年8月', 'value': 16713}, {'legend': '2016年9月', 'value': 15306}, {'legend': '2016年10月', 'value': 16052}],
}
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ret
        raise tornado.gen.Return(result)

    # 工资区间图
    @tornado.gen.coroutine
    def salary_tantile_list(self, job=str, token=str, cache_flag=int):

        result = dict()
        search = job.strip()
        payload = {
            'job_name': search.upper(),
            'search_type': 'salary',
            'job_city': '北京',
            'esapi': self.esapi
        }

        if cache_flag:
            # 读取缓存
            # query_cache_data = None
            query_cache_data = self.cacheredis.get('salary_tantile_list_{search}'.format(search=search.upper()))

            # 读取缓存失败
            if query_cache_data is None:
                th_salary_tantile_list = QueryEsapi.use_query_map(**payload)
            else:
                salary_tantile_list = json.loads(query_cache_data)
                result['status'] = 'success'
                result['token'] = token
                result['msg'] = ''
                result['data'] = salary_tantile_list
                raise tornado.gen.Return(result)
        else:
            th_salary_tantile_list = QueryEsapi.use_query_map(self.esapi, **payload)
        # 处理薪酬区间分布
        salary_tantile_list = th_salary_tantile_list.get()
        salary_tantile_list = [{'legend': salary, 'value': tantile} for \
                               salary, tantile in salary_tantile_list]

        # 平均薪资
        param = {'job_name': search,
                 'esapi': self.esapi}
        th_avg_salary = QueryEsapi.query_job_salary_avg_all(**param)
        if th_avg_salary is None:
            avg_salary = 0
        else:
            avg_salary = th_avg_salary['salary_avg']

        ret = {
            'search': job,
            'salary_tantile_list': salary_tantile_list,
            'avg_salary': avg_salary
            }
        # 加入缓存
        set_cache_data = self.cacheredis.set('salary_tantile_list_{search}'.format(search=search.upper()),
                                             json.dumps(ret), ex=24 * 60 * 60)
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ret
        raise tornado.gen.Return(result)

    # 学历分布图
    @tornado.gen.coroutine
    def edu_tantile_list(self, job=str, token=str, cache_flag=int):

        result = dict()
        search = job.strip()
        payload = {
            'job_name': search.upper(),
            'search_type': 'education',
            'job_city': '北京',
            'esapi': self.esapi
        }

        if cache_flag:
            # 读取缓存
            # query_cache_data = None
            query_cache_data = self.cacheredis.get('edu_tantile_list_{search}'.format(search=search.upper()))

            # 读取缓存失败
            if query_cache_data is None:
                th_salary_tantile_list = QueryEsapi.use_query_map(**payload)
            else:
                salary_tantile_list = json.loads(query_cache_data)
                result['status'] = 'success'
                result['token'] = token
                result['msg'] = ''
                result['data'] = salary_tantile_list
                raise tornado.gen.Return(result)
        else:
            th_salary_tantile_list = QueryEsapi.use_query_map(self.esapi, **payload)
        # 处理薪酬区间分布
        salary_tantile_list = th_salary_tantile_list.get()
        salary_tantile_list = [{'legend': salary, 'value': tantile} for \
                               salary, tantile in salary_tantile_list]

        ret = {'search': job,
               'edu_tantile_list': salary_tantile_list
               }
        # 加入缓存
        set_cache_data = self.cacheredis.set('edu_tantile_list_{search}'.format(search=search.upper()),
                                             json.dumps(ret), ex=24 * 60 * 60)
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ret
        raise tornado.gen.Return(result)

    # 工作年限分布图
    @tornado.gen.coroutine
    def exp_tantile_list(self, job=str, token=str, cache_flag=int):

        result = dict()
        search = job.strip()
        payload = {
            'job_name': search.upper(),
            'search_type': 'work_years',
            'job_city': '北京',
            'esapi': self.esapi
        }

        if cache_flag:
            # 读取缓存
            # query_cache_data = None
            query_cache_data = self.cacheredis.get('exp_tantile_list_{search}'.format(search=search.upper()))

            # 读取缓存失败
            if query_cache_data is None:
                th_salary_tantile_list = QueryEsapi.use_query_map(**payload)
            else:
                salary_tantile_list = json.loads(query_cache_data)
                result['status'] = 'success'
                result['token'] = token
                result['msg'] = ''
                result['data'] = salary_tantile_list
                raise tornado.gen.Return(result)
        else:
            th_salary_tantile_list = QueryEsapi.use_query_map(self.esapi, **payload)
        # 处理薪酬区间分布
        salary_tantile_list = th_salary_tantile_list.get()
        salary_tantile_list = [{'legend': salary, 'value': tantile} for \
                               salary, tantile in salary_tantile_list]
        # 平均工作年限
        param = {
            'job_name': search.upper(),
            'job_city': '北京',
            'area': '',
            'esapi': self.esapi
        }
        th_avg_work_years = QueryEsapi.use_query_avg_work_years(**param)
        avg_work_years = th_avg_work_years.get()
        if avg_work_years is None:
            avg_work_years = 0
        else:
            avg_work_years = avg_work_years
        ret = {'search': job,
               'avg_work_years': avg_work_years,
               'exp_tantile_list': salary_tantile_list
               }
        # 加入缓存
        set_cache_data = self.cacheredis.set('exp_tantile_list_{search}'.format(search=search.upper()),
                                             json.dumps(ret), ex=24 * 60 * 60)
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ret
        raise tornado.gen.Return(result)

    # 高薪行业排行榜图
    @tornado.gen.coroutine
    def trade_salary_list(self, job=str, token=str, cache_flag=int):

        result = dict()
        search = job.strip()
        payload = {
            'job_name': search.upper(),
            'job_city': '北京',
            'area': '',
            'esapi': self.esapi
        }
        if cache_flag:
            # 读取缓存
            # query_cache_data = None
            query_cache_data = self.cacheredis.get('trade_salary_list_{search}'.format(search=search.upper()))

            # 读取缓存失败
            if query_cache_data is None:
                th_trade_salary_list = QueryEsapi.use_query_salary(**payload)
            else:
                salary_tantile_list = json.loads(query_cache_data)
                result['status'] = 'success'
                result['token'] = token
                result['msg'] = ''
                result['data'] = salary_tantile_list
                raise tornado.gen.Return(result)
        else:
            th_trade_salary_list = QueryEsapi.use_query_map(self.esapi, **payload)

        trade_salary_list = th_trade_salary_list.get()
        # 处理高薪行业排行
        trade_salary_list = [{'legend': trade, 'value': salary} for trade, salary in trade_salary_list]
        trade_salary_list = trade_salary_list[:10]
        trade_salary_list.reverse()
        trade_salary_list.sort(key=lambda x:x['value'], reverse=True)
        ret = {'search': job,
               'trade_salary_list': trade_salary_list
               }
        # 加入缓存
        set_cache_data = self.cacheredis.set('trade_salary_list_{search}'.format(search=search.upper()),
                                             json.dumps(ret), ex=24 * 60 * 60)
        result['status'] = 'success'
        result['token'] = token
        result['msg'] = ''
        result['data'] = ret
        raise tornado.gen.Return(result)

    # 活动列表get
    @tornado.gen.coroutine
    def Activity_List(self, cache_flag=int):

        result = dict()
        # tt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = datetime.datetime.now()
        sql_list = "select * from activity where status='open' and end_time>'%s'" % (dt,)
        self.log.info("select * from activity where status='open' and end_time>'%s'" % (dt,))
        search_list = self.db.query(sql_list)
        self.db.close()
        if search_list is not None:
            for index in search_list:
                if index['active_img'] is not None:
                    index['active_img'] = self.image + index['active_img']
                else:
                    index['active_img'] = ''
                if index['active_little_img'] is not None:
                    index['active_little_img'] = self.image + index['active_little_img']
                else:
                    index['active_little_img'] = ''
                    continue
        result['status'] = 'success'
        result['token'] = ''
        result['msg'] = ''
        result['data'] = search_list
        raise tornado.gen.Return(result)

    # 活动post,显示company公司列表
    @tornado.gen.coroutine
    def Activity_Company(self, _id=str, token=str, page=str, num=str, cache_flag=int):

        result = dict()
        num = 20 if int(num) > 20 else int(num)
        sql_active = "select distinct company_id from activity_detail where active_id=%s order by draw_order desc limit %s offset %s" % (_id, int(num), int(page) * int(num))
        search_company = self.db.query(sql_active)
        self.db.close()
        if search_company is not None:
            for num, company_search in enumerate(search_company):
                sql_company_info = "select * from company_detail where id=%s" % company_search['company_id']
                company_info = self.db.get(sql_company_info)
                self.db.close()
                if company_info is None:
                    search_company[num] = {'company_name': '',
                                           'company_trade': '',
                                           'company_scale': '',
                                           'company_type': '',
                                           'company_address': '',
                                           'company_site': '',
                                           'company_logo': '',
                                           'company_id': company_search['company_id']
                                           }
                else:
                    if company_info['company_logo'] != '':
                        logo = "%s" % self.image + company_info['company_logo']
                    else:
                        logo = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                    search_company[num] = {'company_name': company_info['company_name'],
                                           'company_trade': company_info['company_trade'],
                                           'company_scale': company_info['company_scale'],
                                           'company_type': company_info['company_type'],
                                           'company_address': company_info['company_address'],
                                           'company_site': company_info['company_site'],
                                           'company_logo': logo,
                                           'company_id': company_search['company_id']
                                           }

            result['status'] = 'success'
            result['token'] = token
            result['msg'] = ''
            result['data'] = search_company
        raise tornado.gen.Return(result)

    # 活动post,显示job职位列表
    @tornado.gen.coroutine
    def Activity_Job(self, active_id=str, token=str, page=str, num=str, company_id=str, cache_flag=int):

        result = dict()
        num = 20 if int(num) > 20 else int(num)
        if int(company_id) == 0:
            sql_job = "select a.job_name,a.job_city,a.es_id,a.education,a.job_type,a.salary_start,a.salary_end,a.job_city,a.need_num,a.dt_update,c.company_name,c.company_logo" \
                      " from company_jd as a left join activity_detail as b on a.id=b.company_jd_id left join company_detail as c on a.company_user_id=c.company_user_id" \
                      " where b.active_id ='%s' order by dt_update desc limit %s offset %s" % (active_id, num, (int(page) * int(num)))
            search_job = self.db.query(sql_job)
            self.db.close()
            self.log.info("activity,company==0 ++++++++++"+sql_job)
        else:
            sql_job = "select a.job_name,a.job_city,a.es_id,a.education,a.job_type,a.salary_start,a.salary_end,a.job_city,a.need_num,a.dt_update,c.company_name,c.company_logo" \
                      " from company_jd as a left join activity_detail as b on a.id=b.company_jd_id left join company_detail as c on a.company_user_id=c.company_user_id" \
                      " where b.company_id ='%s' order by dt_update desc limit %s offset %s" % (company_id, num, (int(page) * int(num)))
            search_job = self.db.query(sql_job)
            self.db.close()
            self.log.info("activity,company!=0 ++++++++++"+sql_job)
        if search_job is not None:

            for index in search_job:
                index['job_id'] = index.pop('es_id')
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)

                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                # 修改字段为汉字
                if index['job_type'] == 'fulltime':
                    index['job_type'] = '全职'
                elif index['job_type'] == 'parttime':
                    index['job_type'] = '兼职'
                elif index['job_type'] == 'intern':
                    index['job_type'] = '实习'
                elif index['job_type'] == 'unclear':
                    index['job_type'] = '不限'
            result['status'] = 'success'
            result['token'] = token
            result['msg'] = ''
            result['data'] = search_job
        raise tornado.gen.Return(result)

    # 查看收藏
    @tornado.gen.coroutine
    def view_user_collections(self, page=int, num=int, token=str, cache_flag=int):
        if int(num) > 20:
            num = 20
        sql = "select %s from view_user_collections where userid =%s and status='favorite' order by dt_update desc limit %s offset %s"\
              % ("collection_id, userid, jobid, job_name, company_name, company_type, job_type, job_city, boon, work_years_str, trade, scale_str, salary_start, salary_end, education_str, dt_update,company_logo",
                 token, num, (int(page) * int(num)))
        try:
            search_status = self.db.query(sql)
            self.db.close()
            status = 'success'
            for index in search_status:
                index['salary_start'] = index['salary_start'] / 1000
                if (index['salary_end'] % 1000) >= 1:
                    index['salary_end'] = index['salary_end'] / 1000 + 1
                else:
                    index['salary_end'] = index['salary_end'] / 1000
                if index['company_logo'] != '':
                    index['company_logo'] = "%s" % self.image + index['company_logo']
                else:
                    index['company_logo'] = "%s" % self.image + "icompany_logo_%d.png" % (random.randint(1, 16),)
                index['id'] = index['jobid']
                if index['job_type'] == 'fulltime':
                    index['job_type'] = '全职'
                elif index['job_type'] == 'parttime':
                    index['job_type'] = '兼职'
                elif index['job_type'] == 'intern':
                    index['job_type'] = '实习'
                elif index['job_type'] == 'unclear':
                    index['job_type'] = '不限'

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

        result = dict()
        sql = "select count(userid) from view_user_collections where userid =%s and jobid=%s " % (token, job_id)
        sql_ins = "INSERT INTO candidate_collection(user_id, job_id, status, dt_create, dt_update) VALUES (%s,%s,%s,%s,%s)"
        sql_up = "update candidate_collection set status=%s, dt_update=%s" \
                 " where user_id=%s and job_id=%s"

        try:
            # 查找是否收藏
            search_if = self.db.get(sql)
            self.db.close()
            if search_if['count(userid)'] == 0:
                insert_sql = self.db.insert(sql_ins, token, job_id, 'favorite', dt, dt)
                self.db.close()
                result_sql = {'collect': 1}
                msg = '已收藏'
            else:
                # 判断收藏状态（收藏或删除）
                sql_update = "select * from candidate_collection where user_id=%s and job_id=%s" % (token, job_id)
                search_status = self.db.get(sql_update)
                self.db.close()
                if search_status['status'] == "delete":
                    sta = 'favorite'
                    msg = '已收藏'
                    update_db = self.db.update(sql_up, sta, dt, token, job_id)
                    self.db.close()
                    result_sql = {'collect': 1}
                else:
                    sta = 'delete'
                    msg = '已取消收藏'
                    update_db = self.db.update(sql_up, sta, dt, token, job_id)
                    self.db.close()
                    result_sql = {'collect': 0}
            status = 'success'
        except Exception, e:
            self.log.info('ERROR is %s' % e)
            status = 'fail'
            msg = '收藏失败'
            result_sql = {'collect': 2}

        result['status'] = status
        result['token'] = token
        result['msg'] = msg
        result['data'] = result_sql
        raise tornado.gen.Return(result)

    # 取消收藏职位
    @tornado.gen.coroutine
    def user_cancel_collections(self, token=str, job_id=str, cache_flag=int):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = dict()
        sql = "update candidate_collection set status='delete', dt_update=%s" \
                 " where user_id=%s and job_id=%s"
        try:
            search_status = self.db.update(sql, dt, token, job_id)
            self.db.close()
            datas = {'collect': 0}

            result['status'] = 'success'
            result['token'] = token
            result['msg'] = '成功取消收藏'
            result['data'] = datas
        except Exception, e:
            search_status = self.log.info('ERROR is %s' % e)

            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '取消收藏失败'
            result['data'] = {'collect': 2}

        raise tornado.gen.Return(result)

    # 简历投递post
    @tornado.gen.coroutine
    def Post_resume(self, token=str, job_id=str, cache_flag=int):

        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "select * from candidate_post where user_id=%s and job_id=%s" % (token, job_id)

        search_status = self.db.get(sql)
        self.db.close()
        if search_status == None:
            sql_resume = "select allow_post from candidate_cv where user_id=%s" % token
            user_resume = self.db.get(sql_resume)
            self.db.close()
            if (user_resume is None) or (user_resume['allow_post'] == 0):
                result = dict()
                result['status'] = 'fail'
                result['token'] = token
                result['msg'] = '简历信息不完整'
                result['data'] = {'errorcode': 10}
                raise tornado.gen.Return(result)
            else:
                match_rate = random.randint(50, 100)
                status = 'post'
                collect_status = ''
                operate_massage = [{'status': 'post',
                                    'time': dt}]
                sql_post = "insert into candidate_post(user_id, job_id, match_rate," \
                           " status, collect_status, dt_create, dt_update, operate_massage) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                post_resume = self.db.insert(sql_post, token, job_id, match_rate, status, collect_status, dt, dt, json.dumps(operate_massage))
                self.db.close()
                status = 'success'
                msg = '投递成功'
        else:
            result = dict()
            result['status'] = 'fail'
            result['token'] = token
            result['msg'] = '已投递的职位'
            result['data'] = {'errorcode': 20}
            raise tornado.gen.Return(result)
        # 用户投递简历后，公司收到消息
        try:
            sql_company_userid = "select company_user_id from company_jd as j " \
                                 "left join jobs_hot_es_test as p on p.id=j.es_id where p.id =%s" % (job_id,)
            search_company_userid = self.db.get(sql_company_userid)
            self.db.close()
            if search_company_userid is None:
                status = 'success'
                msg = '投递成功'
                self.log.info("User post job , But company_user is None!!!")
            else:
                m_info = {'type': 'post',
                          'info': u'您有新投递的简历'}
                sender = 'system'
                receiver_type = 'company'
                message_type = 'system'
                receiver_user_id = search_company_userid['company_user_id']
                message = json.dumps(m_info)
                sql_company = "insert into message(sender, receiver_type, message_type, receiver_user_id, message, status, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                # self.log.info( "insert into message(sender, receiver_type, message_type, receiver_user_id, message, status, dt_create, dt_update) values(%s,%s,%s,%s,%s,%s,%s,%s)" % (sender, receiver_type, message_type, receiver_user_id,
                #                               message, 'unread', dt, dt))
                post_company = self.db.insert(sql_company, sender, receiver_type, message_type, receiver_user_id,
                                              message, 'unread', dt, dt)
                self.db.close()
                self.log.info('company receive user resume,message_id=%s' % post_company)
        except Exception, e:
            status = 'fail'
            msg = '%s' % e
            post_resume = {'errorcode': 500}
        result = dict()
        result['status'] = status
        result['token'] = token
        result['msg'] = msg
        result['data'] = post_resume
        raise tornado.gen.Return(result)

#   ##### 判断简历
    @tornado.gen.coroutine
    def Judgment_resume(self, token=str):
        sql_status = "select candidate_cv from candidate_cv where user_id=%s" % token
        resume_status = self.db.get(sql_status)
        self.db.close()
        user_cv = json.loads(resume_status['candidate_cv'])

        up_status = "update candidate_cv set allow_post=%s where user_id=%s"
        if user_cv['basic']['name'] == '':
            # 状态写为0
            allow_0 = self.db.update(up_status, 0, token)
            self.db.close()
            self.log.info("candidate_cv allow_post=0; reson-->user_cv['basic']['name'] == ''")
            return 0
        else:
            if user_cv['education'] == []:
                # 状态写为0
                allow_0 = self.db.update(up_status, 0, token)
                self.db.close()
                self.log.info("candidate_cv allow_post=0; reson-->user_cv['education'] == []")
                return 0
            else:
                if user_cv['education'][0]['end_time'] == '':
                    # 状态写为0
                    allow_0 = self.db.update(up_status, 0, token)
                    self.db.close()
                    self.log.info("candidate_cv allow_post=0; reson-->user_cv['education'][0]['end_time'] == ''")
                    return 0
                else:   # 职业意向
                    # if user_cv['intension']['title'] == '':
                    #     # 状态写为0
                    #     allow_0 = self.db.update(up_status, 0, token)
                    #     self.db.close()
                    #     self.log.info("candidate_cv allow_post=0; reson-->user_cv['intension']['school'] == ''")
                    #     return 0
                    # else:
                    # if user_cv['career'] == []: # 实习经历
                    #     # 状态写为0
                    #     allow_0 = self.db.update(up_status, 0, token)
                    #     self.db.close()
                    #     self.log.info("candidate_cv allow_post=0; reson-->user_cv['career'] == []")
                    #     return 0
                    # else:
                    #     if user_cv['career'][0]['end_time'] == '':
                    #         # 状态写为0
                    #         allow_0 = self.db.update(up_status, 0, token)
                    #         self.db.close()
                    #         self.log.info("candidate_cv allow_post=0; reson-->user_cv['career'][0]['end_time'] == ''")
                    #         return 0
                    #     else:
                    # if user_cv['extra']['description'] == '':
                    #     # 状态写为0
                    #     allow_0 = self.db.update(up_status, 0, token)
                    #     self.db.close()
                    #     self.log.info("candidate_cv allow_post=0; reson-->user_cv['extra']['description'] == ''")
                    #     return 0
                    # else:
                        # 状态写为1
                    allow_1 = self.db.update(up_status, 1, token)
                    self.db.close()
                    self.log.info("candidate_cv allow_post=1")
                    return 1

    # ####### 判断是否购买职业导航
    @tornado.gen.coroutine
    def Judgment_invote(self, token=str):
        sql_invote_user = "select * from invite_user where user_id=%s" % (token,)
        invote_user = self.db.get(sql_invote_user)
        # if invote_user =
# ########################################################################

    # 修改数据，慎用
    @tornado.gen.coroutine
    def Edit_datebase(self, cache_flag=int):
        # dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = dict()
        sql_getuser = "select id from candidate_user"
        getuser = self.db.query(sql_getuser)
        self.db.close()
        sql_update = "update candidate_user set user_name=%s,avatar=%s,sex=%s where id=%s"
        for index in getuser:
            try:
                sql_cv = "select username,sex from candidate_cv where user_id=%s" % index['id']
                se_cv = self.db.get(sql_cv)
                self.db.close()
                if se_cv == None:
                    pass
                else:
                    search_st = self.db.update(sql_update, se_cv['username'], "", se_cv['sex'], index['id'])
                    self.db.close()
                    print search_st
            except Exception, e:
                search_status = self.log.info('ERROR is %s' % e)

                result['status'] = 'fail'
                result['token'] = index['id']
                result['msg'] = '数据修改失败'
                result['data'] = search_status
                raise tornado.gen.Return(result)

        raise tornado.gen.Return(result)
# ########################################################################
    # 心跳线
    @tornado.gen.coroutine
    def Idel_database(self, key=str):

        if key == '心跳线2016-9-9':
            # while True:
            cursor = self.db._cursor()
            cursor.execute("show global status like 'Threads_connected';")
            Currently = cursor.fetchone()
            self.db.close()
            # self.db.execute('')

            result = dict()
            result['status'] = 'sucess'
            result['token'] = ''
            result['msg'] = 'Heartbeat!'
            result['data'] = Currently[1]
            raise tornado.gen.Return(result)