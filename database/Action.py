#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import json
import configparser
from api.base_handler import BaseHandler
import logging
# import motor
import tornado
from common.tools import args404, ObjectToString
# from api import base_handler, company_handler, resume_handler, user_handler

# class Action(object):
#     @gen.coroutine
#     def __init__(self, dbhost=str, dbport=int, dbname=str, dbuser=str, dbpwd=str):
#         # pass
#         if dbuser == '':
#             uri = "mongodb://%s:%d/%s" % (dbhost, dbport, dbname)
#         else:
#             uri = "mongodb://%s:%s@%s:%d/%s" % (dbuser, dbpwd, dbhost, dbport, dbname)
#         connection = motor.MotorClient(uri, max_pool_size=500)
#         self.db = connection[dbname]
#         print('init end')



# 用户注册
@tornado.gen.coroutine
def Register_user(mobile=str, pwd=str, cache_flag=int):
    data = dict()
    images = ['http://7xlo2h.com1.z0.glb.clouddn.com/avatar/default_avatar.png']
    data['image'] = images[0]  # [random.randint(0, len(images) - 1)]
    # data['name'] = '用户%s' % (mobile[-6:],)
    data['uuid'] = '8626fa72-4275-11e6-92c4-c81f664404a0'
    data['mobile'] = mobile
    data['pwd'] = pwd
    # name = '用户%s%s' % (mobile[:3],mobile[-3:])# test账号
    user_info = open('D:\\demo\\json_txt\\user.txt','r+')
    write_user = user_info.write(str(data))
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'sucess'
    result['msg'] = ''
    result['token'] = ev_user['uuid']
    result['data'] = ev_user

    raise tornado.gen.Return(result)

# 用户登陆
@tornado.gen.coroutine
def User_login(mobile=str,filepath=str,
                  pwd=str,
                  # umengid=str,
                  # mobibuild=str,
                  # mobitype=str,
                  cache_flag=int):
    user_info = open('%s/user.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    if (ev_user['basic']['mobile'] != mobile) or (ev_user['basic']['pwd'] != pwd):
            result['status'] = 'fail'
            result['token'] = ''
            result['msg'] = '没有此用户!'
            raise tornado.gen.Return(result)

    else:
        result['status'] = 'success'
        result['msg'] = ''
        result['token'] = ev_user['basic']['uuid']
        result['data'] = ev_user
    raise tornado.gen.Return(result)

# 用户登出
@tornado.gen.coroutine
def User_logout(token=str,filepath=str):
    # result = {}
    user_info = open('%s/resume.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    if (ev_user['basic']['uuid'] != token):
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
def User_updatepwd(mobile=str,filepath=str, oldpwd=str, pwd=str, cache_flag=int):

    user_info = open('%s/user.txt'%filepath,'r+')
    for u in user_info.readlines():
        if u == "'pwd':%s" % oldpwd + ',\\n':
            u.replace("'pwd':%s" % oldpwd, "'pwd':%s" % pwd)
        # else:
        #     result = dict()
        #     result['status'] = 'fail'
        #     result['token'] = ''
        #     result['msg'] = '旧密码输入有误'
        #     result['data'] = {}
        #     raise tornado.gen.Return(result)
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = ''
    result['msg'] = '修改密码成功'
    result['data'] = {}
    raise tornado.gen.Return(result)

# 个人信息页
@tornado.gen.coroutine
def Home_user(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/resume-basic.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 首页
@tornado.gen.coroutine
def Home(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/home.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 首页搜索
@tornado.gen.coroutine
def Search_job(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/home.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 消息页，显示数量
@tornado.gen.coroutine
def Job_message(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/message.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = len(ev_user)
    raise tornado.gen.Return(result)

# 简历状态查看get全部
@tornado.gen.coroutine
def Message_all(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/message.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 简历状态查看get被查看
@tornado.gen.coroutine
def Message_viewed(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/message.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    indexs = []
    for index in ev_user:
        try:
            if index['resume_status'] == 'viewed':
                indexs.append(index)
        except Exception, e:
            pass
        #     result = {'status': 'failed',
        #               'token': token,
        #               'msg': '服务器错误',
        #               'data': {}}
        #     raise tornado.gen.Return(result)

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = indexs
    raise tornado.gen.Return(result)

# 简历状态查看get待沟通
@tornado.gen.coroutine
def Message_communicated(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/message.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    indexs = []
    for index in ev_user:
        try:
            if index['resume_status'] == 'communicated':
                indexs.append(index)
        except Exception, e:
            pass
        #     result = {'status': 'failed',
        #               'token': token,
        #               'msg': '服务器错误',
        #               'data': {}}
        #     raise tornado.gen.Return(result)

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = indexs
    raise tornado.gen.Return(result)

# 简历状态查看get面试通过
@tornado.gen.coroutine
def Message_passed(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/message.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    indexs = []
    for index in ev_user:
        try:
            if index['resume_status'] == 'passed':
                indexs.append(index)
        except Exception, e:
            pass
        #     result = {'status': 'failed',
        #               'token': token,
        #               'msg': '服务器错误',
        #               'data': {}}
        #     raise tornado.gen.Return(result)

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = indexs
    raise tornado.gen.Return(result)

# 简历状态查看get不合适
@tornado.gen.coroutine
def Message_improper(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/message.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    indexs = []
    for index in ev_user:
        try:
            if index['resume_status'] == 'improper':
                indexs.append(index)
        except Exception, e:
            pass
        #     result = {'status': 'failed',
        #               'token': token,
        #               'msg': '服务器错误',
        #               'data': {}}
        #     raise tornado.gen.Return(result)

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = indexs
    raise tornado.gen.Return(result)

# 职位详情get
@tornado.gen.coroutine
def Position(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/zhiwei-full.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 公司详情get
@tornado.gen.coroutine
def Company_full(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/company-full.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 简历查看
@tornado.gen.coroutine
def Resume_view(token=str,filepath=str, cache_flag=int):

    user_info = open('%s/resume.txt'%filepath,'r+')
    read_user = user_info.read().decode('gbk')
    ev_user = eval(read_user)
    print ev_user
    user_info.close()

    result = dict()
    result['status'] = 'success'
    result['token'] = token
    result['msg'] = ''
    result['data'] = ev_user
    raise tornado.gen.Return(result)

# 简历编辑-基本信息post
@tornado.gen.coroutine
def Resume_Basic(token=str,filepath=str, data=dict, cache_flag=int):

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
def Resume_Education(token=str,filepath=str, data=dict, cache_flag=int):

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
def Resume_Expect(token=str,filepath=str, data=dict, cache_flag=int):

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
def Resume_Experience(token=str,filepath=str, data=dict, cache_flag=int):

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
def Resume_Item(token=str,filepath=str, data=dict, cache_flag=int):

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
def Resume_Evaluation(token=str,filepath=str, data=dict, cache_flag=int):

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
def Feed_back(token=str,filepath=str, data=dict, cache_flag=int):

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
