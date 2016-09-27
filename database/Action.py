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
    def User_login(self, mobile=str, pwd=str, jiguang_id=str, umeng_id=str, cache_flag=int):
        result = dict()
        sql = "select id,password,user_name,sex,avatar,jiguang_id,umeng_id from candidate_user where phonenum=%s" % mobile
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
        elif (search_mobile['umeng_id'] is None) and (search_mobile['jiguang_id'] is None):
            sql_umeng_jg = "update candidate_user set jiguang_id=%s,umeng_id=%s where phonenum=%s"
            self.db.update(sql_umeng_jg, jiguang_id, umeng_id, mobile)
            self.db.close()
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
                search_mobile.pop('password')
                search_mobile.pop('jiguang_id')
                search_mobile.pop('umeng_id')

                result['status'] = 'success'
                result['msg'] = '登陆成功'
                result['token'] = search_mobile['id']
                result['data'] = search_mobile
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

    # 职为我来post
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
              "left join candidate_post as p on k.id = p.job_id " \
              "left join candidate_user as j on j.id=p.user_id where j.id =%s order by dt_update DESC limit %s offset %s"\
              % ("job_id,company_type,salary_start,salary_end,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str,p.status,p.dt_update,company_logo",
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
              % ("job_id,company_type,salary_start,salary_end,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str,p.status,p.dt_update,company_logo",
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
              % ("job_id,company_type,salary_start,salary_end,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str,p.status,p.dt_update,company_logo",
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
              % ("job_id,company_type,salary_start,salary_end,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str,p.status,p.dt_update,company_logo",
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
              % ("job_id,company_type,salary_start,salary_end,scale_str,job_city,company_name,boon,education_str,job_name,work_years_str,p.status,p.dt_update,company_logo",
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
                              'update_url': ''}
            raise tornado.gen.Return(result)
        else:
            sql_version = "select version,app_file from App_version where status!='delete' order by id desc limit 1 "
            try:
                version_post = self.db.get(sql_version)
                self.db.close()
                self.log.info('-------------------Search version end--')
                version_sql = version_post['version'].split('.')
                isupdate = 0
                for num in xrange(len(version_get)):
                    if version_get[num] > version_sql[num]:
                        isupdate = 1
                        break

            except Exception, e:
                result['status'] = 'fail'
                result['token'] = ''
                result['msg'] = '数据添加不成功'
                result['data'] = {'errorcode': 10,
                                  'isupdate': 0,
                                  'update_url': ''}
                raise tornado.gen.Return(result)
            result['status'] = 'success'
            result['token'] = ''
            result['msg'] = ''
            result['data'] = {'errorcode': 0,
                              'isupdate': isupdate,
                              'update_url': self.image + version_post['app_file']
                              }
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
                    else:
                        if user_cv['intension']['title'] == '':
                            # 状态写为0
                            allow_0 = self.db.update(up_status, 0, token)
                            self.db.close()
                            self.log.info("candidate_cv allow_post=0; reson-->user_cv['intension']['school'] == ''")
                            return 0
                        else:
                            if user_cv['career'] == []:
                                # 状态写为0
                                allow_0 = self.db.update(up_status, 0, token)
                                self.db.close()
                                self.log.info("candidate_cv allow_post=0; reson-->user_cv['career'] == []")
                                return 0
                            else:
                                if user_cv['career'][0]['end_time'] == '':
                                    # 状态写为0
                                    allow_0 = self.db.update(up_status, 0, token)
                                    self.db.close()
                                    self.log.info("candidate_cv allow_post=0; reson-->user_cv['career'][0]['end_time'] == ''")
                                    return 0
                                else:
                                    if user_cv['extra']['description'] == '':
                                        # 状态写为0
                                        allow_0 = self.db.update(up_status, 0, token)
                                        self.db.close()
                                        self.log.info("candidate_cv allow_post=0; reson-->user_cv['extra']['description'] == ''")
                                        return 0
                                    else:
                                        # 状态写为1
                                        allow_1 = self.db.update(up_status, 1, token)
                                        self.db.close()
                                        self.log.info("candidate_cv allow_post=1")
                                        return 1
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

            result = dict()
            result['status'] = 'sucess'
            result['token'] = ''
            result['msg'] = 'Heartbeat!'
            result['data'] = Currently[1]
            raise tornado.gen.Return(result)