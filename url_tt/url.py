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
    UserinfoeditHandler, \
    UseravatareditHandler, \
    MessageHandler, \
    MessageAllHandler, \
    MessageViewedHandler, \
    MessageCommunicatedHandler,\
    MessagePassedHandler, \
    MessageImproperHandler, \
    MessagefullHandler, \
    ViewcollectHandler, \
    AddcollectHandler, \
    CutcollectHandler

from api.position_handler import \
    HomeHandler, \
    SearchHandler, \
    SearchCompanyHandler, \
    PositionHandler, \
    HostsearchlistHandler, \
    HotcityHandler, \
    RecommendjobHandler, \
    SpeedjobHandler

from api.sms_handler import \
    SendSmsHandler, \
    VerifySmsHandler

from api.company_handler import \
    CompanyBasicHandler, \
    CompanyJobHandler, \
    CompanyCompanyHandler, \
    Job500companyHandler

from api.resume_handler import \
    ResumeHandler,\
    ResumeBasicHandler,\
    ResumeEducationHandler,\
    ResumeExpectHandler,\
    ResumeCareerHandler,\
    ResumeEvaluationHandler, \
    PostresumeHandler, \
    ResumeAvatarHandler

from api.tools_handler import \
    FeedbackHandler, \
    GetVersionHandler

from api.Edit_database import \
    EditdatabaseHandler, \
    IdeldatabaseHandler


urls = [
    url(r"/home/page-(\d+)/num-(\d+)/token-(\w+)", HomeHandler),     # 首页get
    url(r"/auth/login", LoginHandler),  # 登录post
    url(r"/auth/logout/token-(\w+)", LogoutHandler),    # 登出get
    url(r"/auth/register", RegisterHandler),    # 注册post
    url(r"/auth/forgetpwd", ForgetpwdHandler),  # 忘记，找回密码
    url(r"/auth/editpwd", UpdatePwdHandler),    # 修改密码post
    url(r"/sendsms", SendSmsHandler),   # 发送短信验证码
    url(r"/job_500company/page-(\d+)/num-(\d+)/token-(\w+)", Job500companyHandler),   # 发送短信验证码
    # url(r"/sendsms/verify/mobile-(\w+)/code-(\w+)", VerifySmsHandler),    # 校验短信验证码(不用)
    url(r"/user-info/edit", UserinfoeditHandler),    # 修改个人信息
    url(r"/user-info/avatar", UseravatareditHandler),    # 修改个人头像
    url(r"/search", SearchHandler),  # 搜索职位post
    url(r"/search-company", SearchCompanyHandler),  # 搜索公司post
    # url(r"/search/company-or-job", SearchCompanyOrJobHandler),  # 搜索公司或者职位名称post(接口用不了)
    url(r"/recommend-job", RecommendjobHandler),  # 推荐职位get
    url(r"/speed-job", SpeedjobHandler),  # 急速招聘post
    url(r"/hot_job/token-(\w+)", HostsearchlistHandler),  # 热门搜索职位列表(先写成固定的)
    url(r"/hot_city/token-(\w+)", HotcityHandler),     # 热门搜索城市列表(先写4个)get
    url(r"/view_collect/page-(\d+)/num-(\d+)/token-(\w+)", ViewcollectHandler),     # 查看收藏get
    url(r"/add_or_del_collect", AddcollectHandler),     # 增加和取消收藏post
    url(r"/cut_collect", CutcollectHandler),     # 取消收藏post(查看收藏中，取消收藏用)
    url(r"/post-resume", PostresumeHandler),     # 简历投递post
    url(r"/message/resume/token-(\w+)", MessageHandler),     # 消息页数量get
    url(r"/message/resume-allstatus/page-(\d+)/num-(\d+)/token-(\w+)", MessageAllHandler),    # 消息(简历状态查看)get全部
    url(r"/message/resume-viewed/page-(\d+)/num-(\d+)/token-(\w+)", MessageViewedHandler),    # 消息(简历状态查看)get被查看
    url(r"/message/resume-communicated/page-(\d+)/num-(\d+)/token-(\w+)", MessageCommunicatedHandler),    # 消息(简历状态查看)get简历通过
    url(r"/message/resume-passed/page-(\d+)/num-(\d+)/token-(\w+)", MessagePassedHandler),    # 消息(简历状态查看)get邀请面试
    url(r"/message/resume-improper/page-(\d+)/num-(\d+)/token-(\w+)", MessageImproperHandler),    # 消息(简历状态查看)get不合适
    url(r"/message-full/job-(\w+)/token-(\w+)", MessagefullHandler),    # 消息详情页，时间轴
    url(r"/position-full/job-(\w+)/token-(\w+)", PositionHandler),    # 职位详情get
    url(r"/company-full/info/company-(\w+)/token-(\w+)", CompanyBasicHandler),    # 公司详情-公司信息get
    url(r"/company-full/company/company-(\w+)/token-(\w+)", CompanyCompanyHandler),    # 公司详情-企业详情get（公司介绍，大事记）
    url(r"/company-full/job", CompanyJobHandler),    # 公司详情-所有职位post
    url(r"/me/token-(\w+)", UserHandler),    # 个人信息页get（基本信息）
    url(r"/resume-view/token-(\w+)", ResumeHandler),    # 简历查看get
    url(r"/resume-edit-avatar", ResumeAvatarHandler),    # 简历编辑-修改头像post
    url(r"/resume-edit-basic", ResumeBasicHandler),    # 简历编辑-基本信息post
    url(r"/resume-edit-education", ResumeEducationHandler),    # 简历编辑-教育经历post(list)
    url(r"/resume-edit-expect", ResumeExpectHandler),    # 简历编辑-职业意向post
    url(r"/resume-edit-career", ResumeCareerHandler),    # 简历编辑-实习经历post(list)
    # ### url(r"/resume-edit-experience", ResumeExperienceHandler),    # 简历编辑-项目社会实践post(先不做)
    # ### url(r"/resume-edit-school_job", ResumeSchooljobHandler),    # 简历编辑-校内职务post(先不做)
    # ### url(r"/resume-edit-school_rewards", ResumeSchoolRewardsHandler),    # 简历编辑-校内奖励post(先不做)
    # ### url(r"/resume-edit-languages", ResumeLanguagesHandler),    # 简历编辑-语言能力post(先不做)
    # ### url(r"/resume-edit-skill", ResumeSkillHandler),    # 简历编辑-IT技能post(先不做)
    # ### url(r"/resume-edit-certificate", ResumeCertificateHandler),    # 简历编辑-获得证书post(先不做)
    url(r"/resume-edit-evaluation", ResumeEvaluationHandler),    # 简历编辑-自我评价post    # extra
    url(r"/feedback", FeedbackHandler),    # 意见反馈post
    url(r"/get-version", GetVersionHandler),    # 获取版本,自动更新（仅Android）
    #   ####################################################################################
    url(r"/idel_database", IdeldatabaseHandler),    # 心跳连接数据库
    url(r"/edit-database/token(\w+)/?", EditdatabaseHandler),    # 修改数据，慎用！！！！！
    url(r"/.*", better404)
    ]