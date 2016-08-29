#! /usr/bin/env python
# -*- coding: utf-8 -*-


from tornado.web import URLSpec as url
from api.user_handler import \
    better404, \
    RegisterHandler, \
    LoginHandler, \
    LogoutHandler, \
    ForgetpwdHandler, \
    UpdatePwdHandler, \
    UserHandler, \
    MessageHandler, \
    MessageAllHandler, \
    MessageViewedHandler, \
    MessageCommunicatedHandler,\
    MessagePassedHandler, \
    MessageImproperHandler, \
    ViewcollectHandler, \
    AddcollectHandler

from api.position_handler import \
    HomeHandler, \
    SearchHandler, \
    PositionHandler, \
    FeedbackHandler, \
    HostsearchlistHandler, \
    HotcityHandler
from api.sms_handler import SendSmsHandler, VerifySmsHandler
from api.company_handler import CompanyHandler

from api.resume_handler import \
    ResumeHandler,\
    ResumeBasicHandler,\
    ResumeEducationHandler,\
    ResumeExpectHandler,\
    ResumeCareerHandler,\
    ResumeItemHandler,\
    ResumeEvaluationHandler, \
    PostresumeHandler

urls = [
    url(r"/home/page-(\d+)/num-(\d+)/token-(\w+)", HomeHandler),     # 首页get
    url(r"/auth/login", LoginHandler),  # 登录post
    url(r"/auth/logout/token-(\w+)", LogoutHandler),    # 登出get
    url(r"/auth/register", RegisterHandler),    # 注册post
    url(r"/auth/forgetpwd", ForgetpwdHandler),  # 忘记，找回密码
    url(r"/auth/editpwd", UpdatePwdHandler),    # 修改密码post
    url(r"/sendsms", SendSmsHandler),   # 发送短信验证码
    # url(r"/sendsms/verify/mobile-(\w+)/code-(\w+)", VerifySmsHandler),    # 校验短信验证码(不用)
    url(r"/search", SearchHandler),  # 搜索页post
    # url(r"/recommend-job/page-(\d+)/num-(\d+)", RecommendjobHandler),  # 推荐职位get
    url(r"/hot_job/token-(\w+)", HostsearchlistHandler),  # 热门搜索职位列表(先写成固定的)
    url(r"/hot_city/token-(\w+)", HotcityHandler),     # 热门搜索城市列表(先写4个)get
    url(r"/view_collect/page-(\d+)/num-(\d+)/token-(\w+)", ViewcollectHandler),     # 查看收藏get
    url(r"/add_or_del_collect", AddcollectHandler),     # 增加和取消收藏post
    # url(r"/cut_collect", CutcollectHandler),     # 取消收藏post(已不用)
    url(r"/post-resume", PostresumeHandler),     # 简历投递post
    url(r"/message/resume/token-(\w+)", MessageHandler),     # 消息页数量get
    url(r"/message/resume-allstatus/page-(\d+)/num-(\d+)/token-(\w+)", MessageAllHandler),    # 消息(简历状态查看)get全部
    url(r"/message/resume-viewed/page-(\d+)/num-(\d+)/token-(\w+)", MessageViewedHandler),    # 消息(简历状态查看)get被查看
    url(r"/message/resume-communicated/page-(\d+)/num-(\d+)/token-(\w+)", MessageCommunicatedHandler),    # 消息(简历状态查看)get已通知
    url(r"/message/resume-passed/page-(\d+)/num-(\d+)/token-(\w+)", MessagePassedHandler),    # 消息(简历状态查看)get面试通过
    url(r"/message/resume-improper/page-(\d+)/num-(\d+)/token-(\w+)", MessageImproperHandler),    # 消息(简历状态查看)get不合适
    url(r"/position-full/job-(\w+)/token-(\w+)", PositionHandler),    # 职位详情get
    url(r"/company-full/company-(\w+)/token-(\w+)", CompanyHandler),    # 公司详情get
    url(r"/me/token-(\w+)", UserHandler),    # 个人信息页get（基本信息）
    url(r"/resume-view/token-(\w+)", ResumeHandler),    # 简历查看get
    # url(r"/resume-edit-basic", ResumeBasicHandler),    # 简历编辑-修改头像post
    url(r"/resume-edit-basic", ResumeBasicHandler),    # 简历编辑-基本信息post
    url(r"/resume-edit-education", ResumeEducationHandler),    # 简历编辑-教育经历post(list)
    url(r"/resume-edit-expect", ResumeExpectHandler),    # 简历编辑-职业意向post
    url(r"/resume-edit-career", ResumeCareerHandler),    # 简历编辑-实习经历post(list)
    # ### url(r"/resume-edit-item", ResumeItemHandler),    # 简历编辑-项目实践post(先不做)
    url(r"/resume-edit-evaluation", ResumeEvaluationHandler),    # 简历编辑-自我评价post
    url(r"/feedback", FeedbackHandler),    # 意见反馈post
    url(r"/.*", better404)
    ]