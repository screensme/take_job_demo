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
    MessageImproperHandler

from api.position_handler import \
    HomeHandler, \
    SearchHandler, \
    PositionHandler, \
    FeedbackHandler

from api.company_handler import \
    CompanyHandler

from api.resume_handler import \
    ResumeHandler,\
    ResumeBasicHandler,\
    ResumeEducationHandler,\
    ResumeExpectHandler,\
    ResumeExperienceHandler,\
    ResumeItemHandler,\
    ResumeEvaluationHandler

urls = [
    url(r"/home", HomeHandler),     # 首页get
    url(r"/auth/login", LoginHandler),  # 登录post
    url(r"/auth/logout/token-(\w+)", LogoutHandler),    # 登出get
    url(r"/auth/register", RegisterHandler),    # 注册post
    # url(r"/auth/forgetpwd", ForgetpwdHandler),  # 忘记密码==修改密码
    url(r"/auth/editpwd", UpdatePwdHandler),    # 修改密码post---hash每次生成不一样
    url(r"/search", SearchHandler),  # 搜索页post√
    # url(r"/send-resume", SendresumeHandler),     # 发送简历post---
    url(r"/message/resume", MessageHandler),     # 消息页数量post
    url(r"/message/resume-allstatus", MessageAllHandler),    # 简历状态查看get全部
    url(r"/message/resume-viewed/token-(\w+)", MessageViewedHandler),    # 简历状态查看get被查看
    url(r"/message/resume-communicated/token-(\w+)", MessageCommunicatedHandler),    # 简历状态查看get待沟通
    url(r"/message/resume-passed/token-(\w+)", MessagePassedHandler),    # 简历状态查看get面试通过
    url(r"/message/resume-improper/token-(\w+)", MessageImproperHandler),    # 简历状态查看get不合适
    url(r"/position-full", PositionHandler),    # 职位详情get
    url(r"/company-full", CompanyHandler),    # 公司详情get
    url(r"/me", UserHandler),    # 个人信息页get（基本信息）
    url(r"/resume-view", ResumeHandler),    # 简历查看get
    url(r"/resume-edit-basic", ResumeBasicHandler),    # 简历编辑-基本信息post
    url(r"/resume-edit-education", ResumeEducationHandler),    # 简历编辑-教育经历post
    url(r"/resume-edit-expect", ResumeExpectHandler),    # 简历编辑-职业意向post
    url(r"/resume-edit-experience", ResumeExperienceHandler),    # 简历编辑-实习经历post
    url(r"/resume-edit-item", ResumeItemHandler),    # 简历编辑-项目实践post
    url(r"/resume-edit-evaluation", ResumeEvaluationHandler),    # 简历编辑-自我评价post
    url(r"/feedback", FeedbackHandler),    # 意见反馈post
    url(r"/.*", better404)
    ]