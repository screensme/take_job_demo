### 此项目为15年刚开始做开发的时候，花了一个多月做的东西（当时需求很急，很多地方比较low，后来也懒得改了），时隔几年之后，原本的项目已经下线，此时把项目开源，做下记录 tornado + mysql。
### 这是一个招聘类的项目，仿以前的拉勾做的，还增加了专家咨询的功能
***
### APP后端API接口文档  
OPEN API接口地址:http://xxx.xxx.xxx:8889/  
测试内网:192.168.12.146  
测试外网:192.168.12.146  
支持格式:json

## 操作记录：
| 时间 | 状态 | 动作 |
| :------| ------ | :------ |
| 9.7-9.12 | 增-改 | 注册、登陆增加了umeng_id和jiguang_id。新建-公司详情的3个接口。新建修改个人头像和简历头像的两个接口 |
| 9.27 | 增-改 | 1.修改了登陆返回的结果，新增umeng_id,jiguang_id,mobile_type,mobile_version,app_version字段，在急速入职中显示佣金根据是否为校园代理proxy_user判断；2.新增，职为我来接口；3.新增，申请成为校园代理接口。 |
|10.13|增|1.增加了活动接口，活动中公司列表 或者 活动中职位列表 的接口|


## url
1.首页get：/home/page-{page}/num-{num}/token-{token}  
2.登录post：/auth/login  
3.登出get：/auth/logout/token-{token}  
4.注册post：/auth/register  
5.修改密码post：/auth/editpwd  
6.搜索页post：/search  
7.消息页get：/message/resume/token-{token}  
8.消息(简历状态)get(全部)：/message/resume-allstatus/page-{page}/num-{num}/token-{token}  
9.消息(简历状态)get(被查看)：/message/resume-viewed/page-{page}/num-{num}/token-{token}  
10.消息(简历状态)get(已通知)：/message/resume-communicated/page-{page}/num-{num}/token-{token}  
11.消息(简历状态)get(面试通过)：/message/resume-passed/page-{page}/num-{num}/token-{token}  
12.消息(简历状态)get(不合适)：/message/resume-improper/page-{page}/num-{num}/token-{token}  
13.职位详情get：/position-full/job-{job_id}/token-{token}  
14.公司详情get：/company-full/company-{company_id}/token-{token}  
15.个人信息页get(基本信息)：/me/token-{token}  
16.简历查看get：/resume-view/token-{token}  
17.简历编辑-基本信息post：/resume-edit-basic  
18.简历编辑-教育经历post：/resume-edit-education  
19.简历编辑-职业意向post：/resume-edit-expect  
20.简历编辑-实习经历post：/resume-edit-career  
21.简历编辑-自我评价post：/resume-edit-evaluation  
22.意见反馈post：/feedback  
23.查看收藏get：/view_collect/page-{page}/num-{num}/token-{token}  
24.增加和删除收藏post：/add_or_del_collect   
25.热门搜索职位列表get：/hot_job/token-{token}  
26.热门搜索城市列表get：/hot_city/token-{token}  
27.简历投递post：/post-resume  
28.忘记，找回密码post：/auth/forgetpwd  
29.短信发送接口post：/sendsms  
30.推荐职位post：/recommend-job
31.消息详情get：/message-full/job-{job_id}/token-{token}  
32.修改个人信息post：/user-info/edit  
33.修改个人头像post：/user-info/avatar  
34.修改简历头像post：/resume-edit-avatar  
35.公司详情-公司信息get：/company-full/info/company-{company_id}/token-{token}  
36.公司详情-企业详情get(公司介绍，大事记)：/company-full/company/company-{company_id}/token-{token}  
37.公司详情-所有职位post：/company-full/job  
38.急速招聘post：/speed-job  
39.搜索公司名post：/search-company  
40.获取版本,自动更新post（仅Android）：/get-version  
41.500强公司get：/job_500company/page-{page}/num-{num}/token-{token}  
42.简历编辑-项目社会实践post：/resume-edit-experience  
43.简历编辑-校内职务post：/resume-edit-school_job  
44.简历编辑-校内奖励post：/resume-edit-school_rewards  
45.简历编辑-获得证书post,put：/resume-edit-certificate  
简历编辑-删除获得证书delete：/resume-del-certificate/cert-{certificate_id}/token-{token}  
46.简历查看V1 get：/resume-view/v1/cv-{cv_id}/token-{token}  
47.职为我来post：/job-for-me  
48.申请成为校园代理get：/application-proxy-user/token-{token}  
49.活动列表get：/activity-list  
50.活动详情post(显示公司/显示职位)：/activity  
51.工资走势图-post：/salary_trend_list(暂时不用)  
52.工资区间图-post：/salary_tantile_list  
53.学历分布图-post：/edu_tantile_list  
54.工作年限分布图-post：/exp_tantile_list  
55.职业导航首页-post：/Pro-navigation  
56.行业职位排行榜-post：/ranking-trade  
57.高薪职位排行榜-post：/ranking-highsalary  
58.热门职位排行榜-post：/ranking-hotjob  
59.高薪行业排行榜图-post：/trade_salary_list  
***
60.职场问答首页-get：/workplaceQA/page-(\d+)/num-(\d+)/token-(\w+)  
61.职场问答首页轮播图-get：/workplaceQA-slide  
62.话题列表-post：/workplaceQA/topic_list  
63.专家详情页-get：/workplaceQA/expert-{expert}/token-{token}  
64.话题详情页-get：/workplaceQA/topic-{topic}/token-{token}  
65.对专家的评价列表-get：/workplaceQA/evaluate/page-{page}/num-{num}/expert-{expert}/token-{token}  
66-1.写评价页-get：/workplaceQA/evaluate  
66-2.写评价页-post：/workplaceQA/evaluate  
67.预约页-post：/workplaceQA/reservation  
68.付款页-post：/workplaceQA/pay  
69.付款成功页-get：/workplaceQA/pay-success/message-{message_id}/token-{token}  
70.新消息列表-get：/message/token-{token}  
71.消息-话题进行中-get：/message/topic-processing/page-{page}/num-{num}/token-{token}  
72.消息-话题待评价-get：/message/topic-evaluated/page-{page}/num-{num}/token-{token}  
73.消息-话题已完成-get：/message/topic-finish/page-{page}/num-{num}/token-{token}  
74.消息-详情-get：/message-full/message-{message_id}/token-{token}  
75.用户自主提问-post：/workplaceQA/question  
76.取消预约、取消付款-post：/workplaceQA/cancel  
***
##### 简历状态：  
	
	名称					状态
	'post'				发送
	'viewed'			被查看
	'pass', 'info'		简历通过
	'notify'			邀请面试(两个状态都属于面试通过)
	'deny'				不合适	

***
##### 收藏状态：  
	
	名称					状态
	取消收藏				0
	已收藏/收藏成功			1
	收藏失败				2	
***
##### 推送自定义返回值：  
	
	名称								状态
	系统消息(push_type)				10
	简历投递状态(push_type)			20

	被查看(push_code)				21
	待沟通(push_code)				22
	面试(push_code)					23
	不合适(push_code)				24
***
## 接口介绍
#### 1.首页get：/home/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
返回结果：（返回的薪资是多少多少K）
```
{
  "status": "success",
  "msg": "",
  "token": "null",
  "data": [
    {
      "scale_str": "",
      "boon": "",
      "company_logo": "",
      "job_type": "不限",
      "job_name": "客户经理",
      "job_city": "北京",
      "salary_start": 2,
      "company_name": "四川长虹电器股份有限公司",
      "salary_end": 3,
	  "need_num": 12,
      "trade": "家具/家电/玩具/礼品",
      "education_str": "本科",
      "id": 163742,
      "work_years_str": "应届毕业生经验",
      "dt_update": "2016-09-26T00:00:00"
    },
    {
      "scale_str": "150-500人",
      "boon": "免费三餐,表现优异有转正机会,百度原始技术团队",
      "company_logo": "",
      "job_type": "实习",
      "job_name": "IOS开发实习生",
      "job_city": "北京",
	  "need_num": 12,
      "salary_start": 3,
      "company_name": "百度作业帮",
      "salary_end": 5,
      "trade": "教育/培训,互联网",
      "education_str": "本科",
      "id": 214643,
      "work_years_str": "实习",
      "dt_update": "2016-08-27T00:00:00"
    }
  ]
}
```  
#### 2.登录post：/auth/login
参数：
		
	参数名称	必填	类型		描述
	mobile		Y	string		手机号
	pwd			Y	string		密码
	jiguang_id	Y	string		极光id
	umeng_id	Y	string		友盟id
返回失败：
```{
  "status": "fail",
  "msg": "登录手机号有误，请重新输入",
  "token": "",
  "data": {}
}
```
返回成功：
```{
  "status": "success",
  "msg": "登陆成功",
  "token": 230,
  "data": {
    "app_version": "9.3.3",		(招聘头条APP版本号)
    "proxy_user": 1,			(1=校园代理,0=普通用户,2=申请代理,3=申请被拒绝)
    "mobile_version": "1.0.1",		(iphone手机版本)
    "mobile_type": "iphone",		(手机型号)
    "umeng_id": "umengid",
    "sex": "",
	"job_id": 0,				(登陆后跳转的职位，0=没有)
    "cv_name": "123456",		(判断是否需要重新填写简历用)
    "jiguang_id": "jiguangid",
    "user_name": "",
    "id": 230,
    "avatar": ""			(头像)
  }
}
```  

#### 3.登出get：/auth/logout/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
返回成功：
```{
  "status": "success",
  "msg": "成功退出登录",
  "token": "123456",
  "data": {}
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "没有此用户!",
  "token": ""
}
```  
#### 4.注册post：/auth/register  
参数：
		
	参数名称	必填	类型		描述
	mobile		Y	string		手机号
	pwd			Y	string		密码
	code		Y	string		验证码
	jiguang_id	Y	string		极光id
	umeng_id	Y	string		友盟id
返回成功：
```{
  "status": "sucess",
  "msg": "",
  "token": 183,
  "data": {
    "token": 183
  }
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "登录手机号有误，请重新输入",
  "token": "",
  "data": {}
}
```  
返回失败2：
```{
  "status": "fail",
  "msg": "手机号已经被注册",
  "token": 183,
  "data": {}
}
```  
#### 5.修改密码post：/auth/editpwd  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	oldpwd		Y	string		旧密码
	pwd			Y	string		密码
返回成功：
```{
  "status": "success",
  "msg": "修改密码成功",
  "token": "",
  "data": {}
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "输入的密码不能为空",
  "token": "",
  "data": {}
}
```  
#### 6.搜索页post：/search  
参数：(可传很多参数，根据参数查询，至少写一个条件)
		
	参数名称			必填	类型			描述
	token				Y	string		用户id
	page				Y	string		页数
	num					Y	string		每页显示数量
	job_name			Y	string		职位名称
	job_type			N	string		全职:"fulltime",兼职/实习:['parttime','intern']
	trade				N	string		行业
	work_years_start(0)	N	string		工作年限
	work_years_end(50)	N	string		工作年限
	job_city			N	string		城市(默认全国)
	area				N	string		区域
	education			N	string		'中专': 2,'大专': 3,'本科': 4,'硕士': 5,'博士': 6
	scale_start(0)		N	string		企业规模
	scale_end(20000)	N	string		企业规模
	company_type(0)		N	string 		企业性质
	salary_start(0)		N	string		薪资范围
	salary_end(200000)	N	string		薪资范围

首页点击全职兼职：  
参数：
		
	参数名称			必填	类型			描述
	token				Y	string		用户id
	page				Y	string		页数
	num					Y	string		每页显示数量
	job_type			Y	string		全职:"fulltime",兼职/实习:['parttime','intern']
返回结果--同其他搜索结果
返回结果：（返回的薪资是多少多少K）
```
{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "scale_str": "500-999人",
      "boon": "五险一金,餐饮补助",
      "company_logo": "",
      "job_type": "全职",
      "job_name": "前端工程师",
      "job_city": "北京",
      "salary_start": 11,
	  "need_num": 12,
      "company_name": "归途如虹",
      "salary_end": 12,
      "trade": "移动互联网/O2O/数据服务",
      "education_str": "本科",
      "id": 214418,
      "work_years_str": "不限",
      "dt_update": "2016-08-19T18:56:53"
    },
    {
      "scale_str": "15-50人",
      "boon": "在安静的校园里一起探索教育的未来",
      "company_logo": "",
      "job_type": "实习",
      "job_name": "前端工程师",
      "job_city": "北京",
	  "need_num": 12,
      "salary_start": 4,
      "company_name": "希悦",
      "salary_end": 9,
      "trade": "互联网,教育/培训",
      "education_str": "不限",
      "id": 214620,
      "work_years_str": "实习",
      "dt_update": "2016-08-26T00:00:00"
    }
  ]
}
```  
#### 7.消息页get：/message/resume/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
返回成功：
```	{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": 4
}
```  
#### 8.消息(简历状态)get(全部)：/message/resume-allstatus/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "18",
  "data": [
    {
      "status": "info",
      "scale_str": "10000人以上",
      "job_id": 214152,
      "company_type": "股份制企业/上市公司",
      "job_city": "北京",
      "salary_start": 0,
      "company_name": "郭路路的公司",
      "salary_end": 0,
      "boon": "年奖季奖,补充保险,年奖季奖",
      "education_str": "中专",
      "job_name": "php大牛1",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:03:07"
    },
    {
      "status": "info",
      "scale_str": "100-499人",
      "job_id": 214229,
      "company_type": "股份制企业/上市公司",
      "job_city": "北京",
      "salary_start": 5000,
      "company_name": "郭路路的公司",
      "salary_end": 9000,
      "boon": "年奖季奖,绩效奖金,股权激励,周末双休",
      "education_str": "不限",
      "job_name": "大神测试",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:03:08"
    }
  ]
}
```  
#### 9.消息(简历状态)get(被查看)：/message/resume-viewed/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量

#### 10.消息(简历状态)get(已通知)：/message/resume-communicated/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量

#### 11.消息(简历状态)get(面试通过)：/message/resume-passed/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量

#### 12.消息(简历状态)get(不合适)：/message/resume-improper/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
 
#### 13.职位详情get：/position-full/job-{job_id}/token-{token}
参数：
		
	参数名称	必填	类型		描述
	job_id		Y	string		职位id
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "68",
  "data": {
    "scale_str": "100-499人",
    "site_name": "智联招聘",
    "collect": 0,	(是否收藏，已收藏1，未收藏0)
    "company_type": "民营",
    "job_type": "全职",
    "need_num": 12,
    "trade": "广告/会展/公关",
    "position_des": "岗位职责： 1、依软件开发需求，完成项目交互程序部分的开发、制作、调试； 2、交互式多媒体系统的开发和部分Flash游戏的程序开发工作；",
    "job_city": "北京",
    "salary_start": 0,
    "company_name": "北京三月雨文化传播有限责任公司",
    "salary_end": 0,
	"company_logo": "",
    "company_address": "北京市海淀区复兴路83号东十二楼401室",
    "resume_post": 1,	(是否投递过简历，已投递1，未投递0)
    "boom": "五险一金,全勤奖,交通补助,通讯补贴,餐补,带薪年假",
    "education_str": "本科",
    "job_name": "软件工程师",
    "dt_update": "2016-04-26T00:00:00"
  }
}
```  
#### 14.公司详情get：/company-full/company-{company_id}/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	company_id	Y	string		公司id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "22",
  "data": {
    "local_company_id": 0,
    "scale": "150-500人",
    "description": "公司简介北京汇能精电科技股份有限公司（股票代码：830996）成立于2007年3月，是国内新能源行业的知名企业，是一家专业从事新能源电源产品研发、制造、销售为一体的北京市高新技术企业。公司坐落昌平区，拥有3000平方的研发大楼；公司于2014年7月在深圳市宝安区创建13000平方的生产制造基地。",
    "post_num": "102200",
    "company_type": "民营公司",
    "site_url": "",
    "local_company_user_id": 0,
    "company_contact": "",
    "company_name": "北京汇能精电科技股份有限公司",
    "dt_create": "2016-03-29T10:44:19",
    "address": "北京市昌平区何营路8号企业墅18号楼",
    "company_trade": "",
    "id": 123909,
    "dt_update": "2016-03-29T10:44:19"
  }
}
```  
#### 15.个人信息页get(基本信息)：/me/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": {
    "username": "邵固",
    "school": "长春教育学院",
    "user_id": 123,
    "age": "26",
    "major": "城乡规划学",
    "sex": "男",
    "edu": "本科",
    "id": 116
  }
}
```  
#### 16.简历查看get：/resume-view/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "168",
  "data": {
    "username": "伏菲",
    "school": "四川现代职业学院",
    "openlevel": "public",
    "user_id": 168,
    "candidate_cv": {
      "intension": {
        "status": "找实习",
        "expect_salary": "10000",
        "trade": "互联网/电子商务",
        "area": "北京",
        "title": "招聘专员"
      },
      "education": [
        {
          "major": "人力资源管理",
          "start_time": "2009.09",
          "end_time": "2013.07",
          "degree": "本科",
          "school": "北京交通大学"
        },
        {
          "major": "中国少数民族语言文化",
          "start_time": "2013.09",
          "end_time": "2016.07",
          "degree": "硕士",
          "school": "北京大学"
        }
      ],
      "certificate": [
        {
          "certificate_name": "英语证书",
          "certificate_time": "2014.06",
          "certificate_level": "英语专业四级"
        },
        {
          "certificate_name": "法语证书",
          "certificate_time": "2015.04",
          "certificate_level": "法语四级证书"
        },
        {
          "certificate_name": "计算机证书",
          "certificate_time": "2015.04",
          "certificate_level": "全国计算机等级三级A"
        }
      ],
      "extra": {
        "description": "本人具有强烈的亲和力，本人具有强烈的亲和力，能流利的使用粤语；做事认真负责，踏实守信，见贤思齐；\n期在外兼职工作，有较强的良好的沟通能力和分析问题解决问题的能力；乐于接\n受挑战，能够适应高强度压力的\n工作，同时具有较强的谈判能力；集体观念强，拥有良好的阿瑟大时代团\n队协作精神和创新意识。撒大叔大叔的",
        "title": ""
      },
      "career": [
        {
          "duty": "1、技术开发中心Sqlserver技术支持；\n2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等；\n3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "title": "开发",
          "start_time": "2013.12",
          "area": "北京",
          "trade": "互联网/电子商务",
          "end_time": "2014.09",
          "company": "滴滴"
        }
      ],
      "school_job": [
        {
          "job_info": "1、技术开发中心Sqlserver技术支持；\n2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等；\n3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "start_time": "2013.07",
          "end_time": "2014.09",
          "job_name": "学生会主席",
          "school_name": "北大"
        },
        {
          "job_info": "1、技术开发中心Sqlserver技术支持；\n2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等；\n3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "start_time": "2014.03",
          "end_time": "2016.03",
          "job_name": "学生会",
          "school_name": "根据业务需求"
        }
      ],
      "experience": [
        {
          "end_time": "2016.02",
          "start_time": "2015.02",
          "project_name": "田园考古",
          "description": "1、技术开发中心Sqlserver技术支持；\n2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等；\n3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "title": "组长"
        }
      ],
      "languages": [
        {
          "readwrite": "熟练",
          "language_name": "英语",
          "hear": "精通"
        },
        {
          "readwrite": "精通",
          "language_name": "日语",
          "hear": "精通"
        },
        {
          "readwrite": "熟练",
          "language_name": "韩语/朝鲜语",
          "hear": "精通"
        }
      ],
      "basic": {
        "marital_status": "未婚",
        "name": "伏菲",
        "gender": "女",
        "politics_status": "群众",
        "phonenum": "15625301984",
        "birthday": 1997,
        "avatar": "",
        "education": "中专",
        "email": "15625301984@163.com",
        "current_area": "北京"
      },
      "skill": [
        {
          "skill_level": "精通",
          "skill_name": "word",
          "skill_time": "12"
        },
        {
          "skill_level": "精通",
          "skill_name": "Java",
          "skill_time": "12"
        },
        {
          "skill_level": "熟练",
          "skill_name": "office",
          "skill_time": "36"
        },
        {
          "skill_level": "熟练",
          "skill_name": "前端",
          "skill_time": "6"
        }
      ],
      "school_rewards": [
        {
          "rewards_name": "二等奖",
          "end_time": "",
          "start_time": "2013.09",
          "school_name": "北京大学",
          "rewards_info": "组织宣传学习“五四”精神，加强班风学风建设，等等，班级一致获得院领导好"
        },
        {
          "rewards_name": "根据业务需求",
          "end_time": "",
          "start_time": "2015.03",
          "school_name": "根据",
          "rewards_info": "1、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；\n2、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；"
        }
      ]
    },
    "age": "19",
    "major": "应用经济学",
    "resume_name": "伏菲的简历",
    "sex": "女",
    "dt_update": "2016-08-18T18:44:31",
    "dt_create": "2016-08-18T18:44:31",
    "edu": "中专",
    "id": 161
  }
}
```  
#### 17.简历编辑-基本信息post：/resume-edit-basic  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	basic		Y	string		用户的基本信息，注意格式如下
<font color=blue>（basic本身是dict格式，将这个dict转换为string格式传过来）如下</font>  
```{
        "education":"中专",
        "birthday":"2010",
        "politics_status":"团员",
        "gender":"男",
        "current_area":"石家庄",
        "name":"赵先生",
        "phonenum":"15638367126",
        "email":"15638367126@163.com",
        "avatar":"avatar_7.png",
        "marital_status":"未婚"
    }
```  
返回成功：
```{
    "status":"success",
    "msg":"",
    "token":"177",
    "data":167
}
```  
#### 18.简历编辑-教育经历post：/resume-edit-education  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	education	Y	string		用户的教育经历，注意格式如下
<font color=blue>（education本身是list格式，将这个list转换为string格式传过来）如下</font>  
```[
    {
        "school":"是对的",
        "start_time":"2015.02",
        "major":"是的",
        "degree":"博士以上",
        "end_time":"2016.02"
    }
]
```  
返回成功：
```
{"status": "success", "msg": "", "token": "177", "data": 167}
```  
#### 19.简历编辑-职业意向post：/resume-edit-expect  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	expect		Y	string		用户的职业意向，注意格式如下
<font color=blue>（expect本身是dict格式，将这个dict转换为string格式传过来）如下</font>
```{
        "trade":"公路/桥梁/铁路/市政/园林景观",
        "title":"结算",
        "area":"朔州",
        "status":"全职",
        "expect_salary":"500000"
    }
```  
返回成功：
```
{"status": "success", "msg": "", "token": "177", "data": 167}
```  
#### 20.简历编辑-实习经历post：/resume-edit-career  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	career		Y	string		用户的实习经历，注意格式如下
<font color=blue>（career本身是list格式，将这个list转换为string格式传过来）如下</font>  
```
[
    {
        "duty":"进入渣打银行总部参观实习",
        "area":"北京",
        "start_time":"2013.03",
        "title":"实习生",
        "trade":"不限",
        "end_time":"2013.04",
        "company":"渣打银行"
    },
    {
        "duty":"总部前台接待",
        "area":"北京",
        "start_time":"2015.01",
        "title":"前台",
        "trade":"房地产",
        "end_time":"2015.02",
        "company":"万科"
    }
]
```  
返回成功：
```
{"status": "success", "msg": "", "token": "177", "data": 167}
```  
#### 21.简历编辑-自我评价post：/resume-edit-evaluation  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	description	Y	string		用户的自我评价
返回成功：
```
{"status": "success", "msg": "", "token": "177", "data": 167}
```  
#### 22.意见反馈post：/feedback  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	info		Y	string		反馈的消息内容
	email		N	string		反馈用户的邮箱（选填）
	feed_type	N	string		1--> APP反馈，2-->问道反馈
返回成功：
```{
  "status": "success",
  "msg": "反馈成功",
  "token": "111",
  "data": {
    "errorcode": 0
  }
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "请输入反馈的内容",
  "token": "",
  "data": {
    "errorcode": 1000
  }
}
```
#### 23.查看收藏get：/view_collect/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "1",
  "data": [
    {
      "education_str": "大专",
      "scale_str": "100-499人",
      "salary_end": 8,
      "userid": 1,
      "company_type": "合资",
      "jobid": 3,
      "job_city": "北京",
      "job_type": "全职",
      "salary_start": 6,
      "company_name": "北京领创鑫业商贸有限公司",
      "boon": "五险一金,年底双薪,交通补助,房补,全勤奖,带薪年假,节日福利,员工旅游",
      "company_logo": "",
      "collection_id": 378,
      "trade": "贸易/进出口",
      "job_name": "财务助理\\会计专员   （月薪8000、朝九晚六、周末双休）",
      "work_years_str": "不限",
      "dt_update": "2016-04-26T00:00:00"
    },
    {
      "education_str": "不限",
      "scale_str": "100-499人",
      "salary_end": 6,
      "userid": 1,
      "company_type": "民营",
      "jobid": 23,
      "job_city": "北京",
      "job_type": "全职",
      "salary_start": 4,
      "company_name": "上海交大昂立国际教育北京首都机场分校",
      "boon": "五险一金,绩效奖金,包吃,包住,带薪年假,员工旅游,节日福利,加班补助",
      "company_logo": "",
      "collection_id": 377,
      "trade": "教育/培训/院校",
      "job_name": "课程顾问",
      "work_years_str": "不限",
      "dt_update": "2016-04-26T00:00:00"
    }
  ]
}
```  
#### 24.增加和删除收藏post：/add_or_del_collect  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	job_id		Y	string		职位id
返回收藏成功：
```{
  "status": "success",
  "msg": "已收藏",
  "token": "1",
  "data": 1
}
```  
返回取消收藏成功：
```{
  "status": "success",
  "msg": "已取消收藏",
  "token": "1",
  "data": 1
}
```  
#### 25.热门搜索职位列表get：/hot_job/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": 1,
  "data": [
    "产品设计师",
    "java",
    "测试工程师",
    "运营专员",
    "运维工程师",
    "产品专员",
    "电商专员",
    "PHP",
    "C++",
    "python"
  ]
}
```  
#### 26.热门搜索城市列表get：/hot_city/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "11",
  "data": {
    "hotcity": [
      "北京",
      "上海",
      "广州",
      "深圳"
    ]
  }
}
```  
#### 27.简历投递post：/post-resume  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	job_id		Y	string		职位id

----返回失败种类： 
	 
	errorcode:10(简历信息不完整)  
	errorcode:20(已投递的职位)  
	errorcode：500(服务器异常)  
返回成功：
```{
  "status": "success",
  "msg": "投递成功",
  "token": "1",
  "data": 1399
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "已投递的职位",
  "token": "1",
  "data": {
	'errorcode':10
	}
}
```  
#### 28.忘记，找回密码post：/auth/forgetpwd  
参数：
		
	参数名称	必填	类型		描述
	mobile		Y	string		手机号
	pwd			Y	string		密码
	code		Y	string		验证码
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": 170,
  "data": {
    "sex": "男",
    "user_name": "屌先生",
    "id": 170,
    "avatar": ""
  }
}
```  
返回失败：  
```{
  "status": "fail",
  "msg": "验证码超时，请重新获取",
  "token": "",
  "data": {
    "token": ""
  }
}
```  
#### 29.短信发送接口post：/sendsms  
参数：
		
	参数名称	必填	类型		描述
	mobile		Y	string		手机号
	key			Y	string		注册(register),找回密码(forgetpwd)
返回成功：  
```{
  "status": "success",
  "msg": "短信发送成功",
  "token": "",
  "data": "111111"
}
```  
返回失败：  
```{
  "status": "fail",
  "msg": "短信发送失败",
  "token": "",
  "data": {}}
  ```  
#### 30.推荐职位post：/recommend-job  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页数量
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": "22",
  "data": [
    {
      "scale_str": "20-99人",
      "boon": "五险一金,交通补助",
      "company_logo": "",
      "job_type": "全职",
      "job_name": "Python",
      "job_city": "北京",
      "salary_start": 20,
      "company_name": "Python软件开发公司",
      "salary_end": 30,
      "trade": "互联网/电子商务",
      "education_str": "大专",
      "id": 214170,
      "work_years_str": "不限",
      "dt_update": "2016-07-29T17:09:47"
    },
    {
      "scale_str": "",
      "boon": "五险一金,交通补助",
      "company_logo": "",
      "job_type": "全职",
      "job_name": "Python",
      "job_city": "北京",
      "salary_start": 20,
      "company_name": "",
      "salary_end": 30,
      "trade": "",
      "education_str": "大专",
      "id": 214199,
      "work_years_str": "",
      "dt_update": "2016-07-29T00:00:00"
    }
  ]
}
```
#### 31.消息详情get：/message-full/job-{job_id}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	job_id		Y	string		职位id
！！备注：状态依次是：投递简历，被查看，过初筛，邀请面试，面试不合适。
公司可能会不查看，直接下载简历，这样就会没有被查看的状态。  
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": "20",
  "data": [
    {
      "status": "post",
      "time": "2016-08-31 15:57:45"
    },
    {
      "status": "pass",
      "time": "2016-08-31 15:57:53"
    },
    {
      "status": "info",
      "time": "2016-08-31 15:58:01"
    },
    {
      "status": "notify",
      "username": "赵辰磊",		(个人用户名)
      "invite_time": "2016-11-11 08:12",	(邀请面试时间)
      "address": "北京",		(面试地点)
      "invite_type": "笔试邀请",
      "content": "带简历，带笔参加笔试",		(面试要求)
      "phone": "18031269672",		（企业联系人的联系方式）
      "contact": "赵",		(企业用户名)
      "company_name": "京东",		（公司名）
      "time": "2016-08-31 15:58:39",	（操作时间）
      "job_name": "php",		（职位名称）
      "subject": "php"		（职位标题）
    }
  ]
}
```  
#### 32.修改个人信息post：/user-info/edit  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	sex			Y	string		性别
	avatar		Y	string		头像（第一版传空字符串）
	user_name	Y	string		用户名
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": "170",
  "data": 1
}
```  
#### 33.修改个人头像post：/user-info/avatar  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	avatar		Y	string		头像（文件名xxx.png）
返回成功：  
```{
  "status": "success",
  "msg": "修改个人头像成功",
  "token": "238",
  "data": {}
}
```  
#### 34.修改简历头像post：/resume-edit-avatar  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	avatar		Y	string		头像（文件名xxx.png）
返回成功：  
```{
  "status": "success",
  "msg": "修改简历头像成功",
  "token": "238",
  "data": {}
}
```  
#### 35.公司详情-公司信息get：/company-full/info/company-{company_id}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	company_id	Y	string		公司id
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": "1",
  "data": {
    "company_logo": "http://imgtest.zhaopintt.com/icompany_logo_13.png",
    "company_type": "私营/民营企业",
    "company_scale": "50-99人",
    "company_name": "北京鑫嵘科技有限公司",
    "company_site": "",
    "company_trade": ""
  }
}
```  
返回错误:
```{
  "status": "fail",
  "msg": "没有公司详情!",
  "token": "1",
  "data": {
    "errorcode": 1001
  }
}
```  
#### 36.公司详情-企业详情get(公司介绍，大事记)：/company-full/company/company-{company_id}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	company_id	Y	string		公司id
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": "1",
  "data": {
    "picture": [],
    "company_id": "",
    "boon": "",
    "company_address": "北京朝阳区顺白路甲12号",
    "company_des": "北京后盾计算机技术培训有限责任公司是专注于培养中国互联网优秀的程序语言专业人才的专业型培训机构。后盾网是一个致力于互联网领域建设的资深开发型团队，现多个成员在担任外资集团、企事业单位的网络顾问职务。团队还曾多次为国内外上市集团、政府机关的大型项目提供技术支持，其中包括新浪、搜狐、腾讯、保洁公司、联想、丰田、北京工商银行、FLUCK、ANSYS、长安汽车、新思路模特、中国一汽等众多大众所熟知的知名企业。从团队建设至今，我们积累了大量的团队协",
    "events": ""
  }
}
```  
返回错误:
```{
  "status": "fail",
  "msg": "没有公司详情!",
  "token": "1",
  "data": {
    "errorcode": 1001
  }
}
```  
#### 37.公司详情-所有职位post：/company-full/job  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id
	page			Y	string		页数
	num				Y	string		每页数量
	job_type		Y	string		部门名称(默认请填写"全部")
	company_id		Y	string		公司id
	company_name	Y	string		公司名称
返回成功：  
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": {
    "department": [
      "全部",
      "111111111111111",
      "开发部",
      "市场部",
      "grhg"
    ],
    "job": [
      {
        "job_id": 214423,
        "job_type": "兼职",
        "need_num": 10,
        "job_city": "北京",
        "salary_start": 9,
        "dt_update": "2016-08-19T19:50:16",
        "salary_end": 11,
        "department": "",
        "education_str": "不限",
        "job_name": "发单员"
      },
      {
        "job_id": 214421,
        "job_type": "全职",
        "need_num": 2,
        "job_city": "北京",
        "salary_start": 7,
        "dt_update": "2016-08-19T19:05:42",
        "salary_end": 12,
        "department": "grhg",
        "education_str": "不限",
        "job_name": "g4g"
      }
    ]
  }
}
```  
返回错误:
```{
  "status": "fail",
  "msg": "没有公司详情!",
  "token": "1",
  "data": {
    "errorcode": 1001
  }
}
```  
#### 38.急速招聘post：/speed-job   
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id
	page			Y	string		页数
	num				Y	string		每页数量
	job_type		Y	string		全职:"fulltime",兼职/实习['parttime','intern']
返回成功：（同首页和职位推荐页的返回结果）
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "scale_str": "100-499人",
      "boon": "五险一金",
	  "commission": 0,			(佣金字段，0=没有佣金)
	  "commission_type": "100/次",	(新佣金字段，"0"=没有佣金，)
      "company_logo": "http://imgtest.zhaopintt.com/company_logo_596.jpeg",
      "job_type": "全职",
      "need_num": 12,
      "job_name": "人力资源专员",
      "job_city": "北京",
      "salary_start": 12,
      "company_name": "测试",
      "salary_end": 14,
      "trade": "互联网/电子商务",
      "education_str": "不限",
      "id": 214679,
      "work_years_str": "不限",
      "dt_update": "2016-09-12T18:52:45"
    },
    {
      "scale_str": "100-499人",
      "boon": "五险一金",
	  "commission": 0,			(佣金字段，0=没有佣金，一般用户看到也为0)
	  "commission_type": "0",		(新佣金字段，"0"=没有佣金，)
      "company_logo": "http://imgtest.zhaopintt.com/company_logo_596.jpeg",
      "job_type": "全职",
      "need_num": 12,
      "job_name": "php",
      "job_city": "北京",
      "salary_start": 12,
      "company_name": "测试",
      "salary_end": 12,
      "trade": "互联网/电子商务",
      "education_str": "不限",
      "id": 214678,
      "work_years_str": "不限",
      "dt_update": "2016-09-12T00:00:00"
    }
  ]
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "",
  "token": "123",
  "data": []
```
#### 39.搜索公司名post：/search-company  
		
	参数名称			必填	类型			描述
	token				Y	string		用户id
	page				Y	string		页数
	num					Y	string		每页显示数量
	company_name		Y	string		公司名称
	job_type			N	string		全职:"fulltime",兼职/实习:['parttime','intern']
	trade				N	string		行业
	work_years_start(0)	N	string		工作年限
	work_years_end(50)	N	string		工作年限
	job_city			N	string		城市(默认全国)
	area				N	string		区域
	education			N	string		'中专': 2,'大专': 3,'本科': 4,'硕士': 5,'博士': 6
	scale_start(0)		N	string		企业规模
	scale_end(20000)	N	string		企业规模
	company_type(0)		N	string 		企业性质
	salary_start(0)		N	string		薪资范围
	salary_end(200000)	N	string		薪资范围
返回结果：（返回的薪资是多少多少K）
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "scale_str": "规模500人以上",
      "boon": "养老保险,失业保险,医疗保险,生育保险,工伤保险,住房公积金,包住",
      "company_logo": "http://imgtest.zhaopintt.com/icompany_logo_2.png",
      "job_type": "全职",
      "job_name": "链家新房置业顾问",
      "job_city": "北京市 东城区",
      "salary_start": 3,
      "company_name": "链家新房",
      "salary_end": 5,
      "trade": "",
      "education_str": "高中",
      "id": 175827,
      "work_years_str": "经验不限",
      "dt_update": "2016-09-06T10:16:27"
    },
    {
      "scale_str": "规模500人以上",
      "boon": "养老保险,失业保险,医疗保险,生育保险,工伤保险,住房公积金,年终奖",
      "company_logo": "http://imgtest.zhaopintt.com/icompany_logo_16.png",
      "job_type": "全职",
      "job_name": "顺义链家招聘销售同业优先",
      "job_city": "北京市 东城区",
      "salary_start": 5,
      "company_name": "北京链家房地产经纪有限公司 -h7f",
      "salary_end": 8,
      "trade": "中介服务",
      "education_str": "高中",
      "id": 98647,
      "work_years_str": "经验不限",
      "dt_update": "2015-11-26T00:00:00"
    }
  ]
}
```  
#### 40.获取版本,自动更新post（仅Android）：/get-version  
参数：
		
	参数名称		必填	类型		描述
	Version			Y	string		版本号(大写V，格式：1.0.2)
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "",
  "data": {
    "errorcode": 0,		(0表示成功)
    "update_url": "www.baidu.com",		（下载地址）
	'version': "1.0.9"
    "isupdate": 1		（1表示需要更新，0表示不需要更新）
  }
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "非安卓手机",
  "token": "",
  "data": {
    "errorcode": 1000,
    "update_url": "",
	'version': '',
    "isupdate": 0
  }
}
```  
#### 41.500强公司get：/job_500company/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称		必填	类型		描述
	page			Y	string		页数（0开始）
	num				Y	string		每页数量
	token			Y	string		用户id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "11",
  "data": [
    {
      "url": "https://campus.alibaba.com/index.htm",
      "logo": "http://imgtest.zhaopintt.com/job_500company_logo_32.png",
      "f_home": 1,
      "company_name": "阿里巴巴",
      "logo_mobile": "http://imgtest.zhaopintt.com/job_500company_logo_32.png"
    },
    {
      "url": "http://career.cmbchina.com/",
      "logo": "http://imgtest.zhaopintt.com/job_500company_logo_55.png",
      "f_home": 2,
      "company_name": "招商银行",
      "logo_mobile": "http://imgtest.zhaopintt.com/job_500company_logo_55.png"
    }
  ]
}
```  
#### 42.简历编辑-项目社会实践post：/resume-edit-experience  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	experience	Y	string		用户的项目经历，注意格式如下
<font color=blue>（education本身是list格式，将这个list转换为string格式传过来）如下</font>  
```[
        {
            "project_name":"田园考古",
            "end_time":"2016.02",
            "title":"组长",
            "start_time":"2015.02",
            "description":"1、技术开发中心Sqlserver技术支持
        }
    ]
```  
返回成功：
```{
  "status": "success",
  "msg": "项目经历修改成功",
  "token": "170",
  "data": {
    "errorcode": 0
  }
}
```  
#### 43.简历编辑-校内职务post：/resume-edit-school_job  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	school_job	Y	string		用户的校内职务，注意格式如下
<font color=blue>（education本身是list格式，将这个list转换为string格式传过来）如下</font>  
```[
        {
            "job_info":"1、技术开发中心Sqlserver技术支持； 2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等； 3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
            "start_time":"2013.07",
            "end_time":"2014.09",
            "job_name":"学生会主席",
            "school_name":"北大"
        },
        {
            "job_info":"1、技术开发中心Sqlserver技术支持； 2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等； 3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
            "start_time":"2014.03",
            "end_time":"2016.03",
            "job_name":"学生会",
            "school_name":"根据业务需求"
        }
    ]
```  
```{
  "status": "success",
  "msg": "校内职位修改成功",
  "token": "170",
  "data": {
    "errorcode": 0
  }
}
```  
#### 44.简历编辑-校内奖励post：/resume-edit-school_rewards  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	school_rewards	Y	string		用户的校内奖励，注意格式如下
<font color=blue>（education本身是list格式，将这个list转换为string格式传过来）如下</font>  
```[
        {
            "end_time":"",
            "start_time":"2013.09",
            "rewards_name":"二等奖",
            "school_name":"北京大学",
            "rewards_info":"组织宣传学习“五四”精神，加强班风学风建设，等等，班级一致获得院领导好"
        },
        {
            "end_time":"",		# 这个传空
            "start_time":"2015.03",
            "rewards_name":"根据业务需求",
            "school_name":"根据",
            "rewards_info":"1、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理； 2、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理； 1 1 1"
        }
    ]
```  
返回成功：
```{
  "status": "success",
  "msg": "校内奖励修改成功",
  "token": "170",
  "data": {
    "errorcode": 0
  }
}
```  
#### 45.简历编辑-获得证书(post,put,delete)：/resume-edit-certificate  

简历编辑-新建获得证书post：/resume-edit-certificate  
参数：
		
	参数名称			必填	类型		描述
	token				Y	string		用户id	
	cv_id				Y	string		用户简历id
	certificate_name	Y	string		证书名称
	certificate_image	Y	string		证书图片名字(cert_token_时间戳.png)

简历编辑-编辑获得证书put：/resume-edit-certificate  
参数：
		
	参数名称			必填	类型		描述
	token				Y	string		用户id	
	certificate_id		Y	string		用户简历id
	certificate_name	Y	string		证书名称
	certificate_image	Y	string		证书图片名字(cert_token_时间戳.png)

简历编辑-删除获得证书delete：/resume-del-certificate/cert-{certificate_id}/token-{token}  
参数：
		
	参数名称			必填	类型		描述
	token				Y	string		用户id	
	certificate_id		Y	string		用户简历id

返回成功：
```{
  "status": "success",
  "msg": "获得证书新建成功",
  "token": "170",
  "data": {
    "errorcode": 0
  }
}
```
#### 46.简历查看V1 get：/resume-view/v1/cv-{cv_id}/token-{token}  
参数：
		
	参数名称			必填	类型		描述
	token				Y	string		用户id	
	cv_id				Y	string		用户简历id(现在传这个'Noneid')
返回成功：（证书"certificate"有变化）
```{
  "status": "success",
  "msg": "",
  "token": "170",
  "data": {
    "openlevel": "public",
    "user_id": 170,
	"userclass": "网络"		
    "candidate_cv": {
      "intension": {
        "status": "兼职/实习",
        "expect_salary": "5k-10k",
        "title": "php",
        "trade": "互联网",
        "area": "上海ysyeyey"
      },
      "education": [
        {
          "start_time": "2012.02",
          "end_time": "2014.09",
		  "classroom": '计算机2008届',		(新添加的字段，班级)
          "major": "sdafasd",
          "degree": "本科",
          "school": "aaaaaaeeeeee"
        },
        {
          "start_time": "2011.09",
          "end_time": "2015.06",
		  "classroom": '计算机2008届',		(新添加的字段，班级)
          "major": "计算机科学与技术",
          "degree": "本科",
          "school": "石家庄rrrrrr"
        }
      ],
      "certificate": [				(这里有变化)
        {
          "certificate_name": "英语专业四级",
          "id": 1,						(证书id，会用到字段为certificate_id)
          "certificate_image": "avatar_1"
        },
        {
          "certificate_name": "英语专业流级",
          "id": 2,						(证书id，会用到字段为certificate_id)
          "certificate_image": "avatar_2"
        }
      ],
      "extra": {
        "description": "",
        "title": ""
      },
      "career": [
        {
          "duty": "",
          "area": "",
          "start_time": "",
          "title": "",
          "trade": "",
          "end_time": "",
          "company": ""
        }
      ],
      "school_job": [
        {
          "job_info": "1、技术开发中心Sqlserver技术支持； 2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等； 3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "start_time": "2013.07",
          "end_time": "2014.09",
          "job_name": "学生会主席",
          "school_name": "北大"
        },
        {
          "job_info": "1、技术开发中心Sqlserver技术支持； 2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等； 3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "start_time": "2014.03",
          "end_time": "2016.03",
          "job_name": "学生会",
          "school_name": "根据业务需求"
        }
      ],
      "experience": [
        {
          "title": "组长",
          "start_time": "2015.02",
          "project_name": "田园考古",
          "description": "1、技术开发中心Sqlserver技术支持； 2、数据库环境安装、升级，日常管理，性能优化和监控，调优，备份，恢复测试，迁移，故障处理等； 3、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理；",
          "end_time": "2016.02"
        }
      ],
      "languages": [
        {
          "readwrite": "",
          "language_name": "",
          "hear": ""
        }
      ],
      "basic": {
        "politics_status": "团员",
        "gender": "男",
        "marital_status": "未婚",
        "phonenum": "15801616013",
        "birthday": "1990",
        "avatar": "",
        "current_area": "33333",
        "education": "本科",
        "email": "xsn@huoban.io",
        "name": "徐帅楠"
      },
      "skill": [
        {
          "skill_time": "",
          "skill_name": "",
          "skill_level": ""
        }
      ],
      "school_rewards": [
        {
          "start_time": "2013.09",
          "school_name": "北京大学",
          "end_time": "",
          "rewards_name": "二等奖",
          "rewards_info": "组织宣传学习“五四”精神，加强班风学风建设，等等，班级一致获得院领导好"
        },
        {
          "start_time": "2015.03",
          "school_name": "根据",
          "end_time": "",
          "rewards_name": "根据业务需求",
          "rewards_info": "1、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理； 2、根据业务需求，参与数据库的架构设计和数据结构的优化、模型设计、容量等管理； 1 1 1"
        }
      ]
    },
    "allow_post": 0,
    "dt_update": "2016-09-23T15:46:26",
    "dt_create": "2016-08-25T14:26:21",
    "id": 167						(简历的id，会用到字段名称cv_id)
  }
}
```  
#### 47.职为我来post：/job-for-me  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	page		Y	string		页数
	num			Y	string		每页数量（num>=20，显示20）
返回结果数据结构同首页  
#### 48.申请成为校园代理get：/application-proxy-user/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回结果：
```{
  "status": "success",
  "msg": "申请成功，我们会尽快联系您",
  "token": "231",
  "data": {
    "errorcode": 0		(10=没有此用户,20=重复提交,50=简历不完整,1000=服务器错误)
  }
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "已经申请校园代理，请不要重复提交",
  "token": "231",
  "data": {
    "errorcode": 20		(10=没有此用户,20=重复提交,50=简历不完整,1000=服务器错误)
  }
}
```  
#### 49.活动列表get：/activity-list  
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "",
  "data": [
    {
      "status": "open",
      "active_color": "#99343",
      "start_time": "2016-10-11T00:00:00",
      "active_city": "北京",
      "active_name": "2016秋季招聘会",
	  "active_little_img": "",		(手机端小图)
      "active_img": "http://imgtest.zhaopintt.com/activiry_1.jpeg",	(活动大图)
      "end_time": "2016-10-14T00:00:00",
      "dt_create": "2016-10-11T12:05:47",
      "id": 1,		(活动id)
      "dt_update": "2016-10-11T12:08:37"
    },
    {
      "status": "open",
      "active_color": "#87656",
      "start_time": "2016-10-11T00:00:00",
      "active_city": "全国",
      "active_name": "华北会计专场招聘会",
	  "active_little_img": "",		(手机端小图)
      "active_img": "http://imgtest.zhaopintt.com/activiry_2.jpeg",	(活动大图)
      "end_time": "2016-10-14T00:00:00",
      "dt_create": "2016-10-11T12:07:38",
      "id": 2,
      "dt_update": "2016-10-11T12:08:27"
    }
  ]
}
```
#### 50.活动详情post(显示公司/显示职位)：/activity  
参数：
		
	参数名称	必填	类型		描述
	active_id			Y	string		活动id	
	company_id	Y	string		公司id	(点击单个公司查看职位列表填写公司id,其他填写0)
	token		Y	string		用户id	
	key_type	Y	string		company或job(company显示公司列表,job显示职位列表)	
	page		Y	string		页数	
	num			Y	string		每页数量	
返回公司列表：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "company_scale": "20人以下",
      "company_name": "测试公司1",
      "company_address": "中关村",
      "company_id": 12,
      "company_logo": "http://imgtest.zhaopintt.com/icompany_logo_13.png",
      "company_type": "国有企业",
      "company_site": "",
      "company_trade": "互联网/电子商务"
    }
  ]
}
```

返回职位列表：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "job_id": 214113,
      "company_logo": "http://imgtest.zhaopintt.com/company_logo_2.png",
      "job_type": "兼职",
      "company_name": "hello worldasf",
      "need_num": 1,
      "job_city": "北京",
      "salary_start": 10,
      "dt_update": "2016-07-29T17:44:59",
      "salary_end": 20,
      "education": "1",
      "job_name": "Python"
    }
  ]
}
```

点击公司查看职位列表：
```
{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "job_id": 214113,
      "company_logo": "http://imgtest.zhaopintt.com/company_logo_2.png",
      "job_type": "兼职",
      "company_name": "hello worldasf",
      "need_num": 1,
      "job_city": "北京",
      "salary_start": 10,
      "dt_update": "2016-07-29T17:44:59",
      "salary_end": 20,
      "education": "1",
      "job_name": "Python"
    }
  ]
}
```  

#### 51.工资走势图-post：/salary_trend_list  (暂时不用)
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	job			Y	string		职业名称
返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": {
    "salary_trend_list": [
      {
        "legend": "2015年11月",
        "value": 16174
      },
      {
        "legend": "2015年12月",
        "value": 15513
      },
      {
        "legend": "2016年1月",
        "value": 15426
      },
      {
        "legend": "2016年2月",
        "value": 15808
      },
      {
        "legend": "2016年3月",
        "value": 16636
      },
      {
        "legend": "2016年4月",
        "value": 16358
      },
      {
        "legend": "2016年5月",
        "value": 15890
      },
      {
        "legend": "2016年6月",
        "value": 15973
      },
      {
        "legend": "2016年7月",
        "value": 16443
      },
      {
        "legend": "2016年8月",
        "value": 16713
      },
      {
        "legend": "2016年9月",
        "value": 15306
      },
      {
        "legend": "2016年10月",
        "value": 16052
      }
    ],
    "search": "python"
  }
}
```  

#### 52.工资区间图-post：/salary_tantile_list  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	job			Y	string		职业名称
返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": {
    "search": "python",
    "avg_salary": '14960元/月',
    "salary_tantile_list": [
      {
        "legend": "3k以下",
        "value": 0.85
      },
      {
        "legend": "3k-5k",
        "value": 1.69
      },
      {
        "legend": "5k-8k",
        "value": 4.51
      },
      {
        "legend": "8k-12k",
        "value": 37.75
      },
      {
        "legend": "12k-15k",
        "value": 4.51
      },
      {
        "legend": "15k-20k",
        "value": 22.25
      },
      {
        "legend": "20k-25k",
        "value": 8.45
      },
      {
        "legend": "25k-30k",
        "value": 1.41
      },
      {
        "legend": "30k-40k",
        "value": 0.28
      },
      {
        "legend": "40k-50k",
        "value": 0.28
      },
      {
        "legend": "50k以上",
        "value": 0
      }
    ]
  }
}
```  

#### 53.学历分布图-post：/edu_tantile_list  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	job			Y	string		职业名称
返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": {
    "search": "python",
    "edu_tantile_list": [
      {
        "legend": "中专",
        "value": 7.4
      },
      {
        "legend": "大专",
        "value": 22.19
      },
      {
        "legend": "本科",
        "value": 69.45
      },
      {
        "legend": "硕士",
        "value": 0.96
      },
      {
        "legend": "博士",
        "value": 0
      }
    ]
  }
}
```  

#### 54.工作年限分布图-post：/exp_tantile_list  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	job			Y	string		职业名称
返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": {
    "avg_work_years": '2年',
    "search": "python",
    "edu_tantile_list": [
      {
        "legend": "应届毕业生",
        "value": 5.59
      },
      {
        "legend": "1-3年",
        "value": 52.8
      },
      {
        "legend": "3-5年",
        "value": 38.46
      },
      {
        "legend": "5-10年",
        "value": 3.15
      },
      {
        "legend": "10年以上",
        "value": 0
      }
    ]
  }
}
```  

#### 55.职业导航首页-post：/Pro-navigation  
参数：
		
	参数名称	必填	类型		描述
	token			Y	string		用户id	
	invite_code		Y	string		导航邀请码(默认传'',用户手动输入的邀请码)
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": {
    "trade_list": [
      {
        "trade_name": "银行",
        "id": 1
      },
      {
        "trade_name": "食品/饮料",
        "id": 2
      },
      {
        "trade_name": "智能硬件",
        "id": 3
      }
    ],
    "major_list": [
      {
        "major_name": "highsalary"
      },
      {
        "major_name": "hotjob"
      }
    ]
  }
}
```  
返回失败：
```{
  "status": "success",
  "msg": "",
  "token": "230",
  "data": {
    "errorcode": 10,
    "trade_list": [
      {
        "trade_name": "金融/银行/证券",
        "id": 1
      },
      {
        "trade_name": "通信/电子",
        "id": 2
      },
      {
        "trade_name": "市场/销售/客服",
        "id": 3
      },
      {
        "trade_name": "房地产/建筑",
        "id": 4
      },
      {
        "trade_name": "人力/行政/后勤",
        "id": 5
      },
      {
        "trade_name": "设计/广告/媒体/艺术",
        "id": 6
      }
    ],
    "major_list": [
      {
        "major_name": "highsalary"
      },
      {
        "major_name": "hotjob"
      }
    ]
  }
}
```  
#### 56.行业职位排行榜-post：/ranking-trade  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	trade		Y	string		行业名称(将职业导航首页的行业写入)
返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "salary_avg": "16351元/月",
      "job_name": "数据挖掘"
    },
    {
      "salary_avg": "13003元/月",
      "job_name": "产品经理"
    },
    {
      "salary_avg": "4572元/月",
      "job_name": "出纳"
    }
  ]
}
```  
#### 57.高薪职位排行榜-post：/ranking-highsalary  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	

返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "salary_avg": "18900元/月",
      "job_name": "算法工程师"
    },
    {
      "salary_avg": "14007元/月",
      "job_name": "IOS"
    },
    {
      "salary_avg": "13935元/月",
      "job_name": "交互设计师"
    },
    {
      "salary_avg": "4191元/月",
      "job_name": "生产技工"
    }
  ]
}
```  
#### 58.热门职位排行榜-post：/ranking-hotjob  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	

返回结果：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "salary_avg": "15269元/月",
      "job_name": "产品经理"
    },
    {
      "salary_avg": "8909元/月",
      "job_name": "HRBP"
    },
    {
      "salary_avg": "7376元/月",
      "job_name": "UI"
    },
    {
      "salary_avg": "6025元/月",
      "job_name": "运营专员"
    },
    {
      "salary_avg": "5304元/月",
      "job_name": "招聘专员"
    }
  ]
}
```  
#### 59.高薪行业排行榜图-post：/trade_salary_list  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	job			Y	string		职位名称
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": {
    "search": "行政文员",
    "trade_salary_list": [
      {
        "legend": "广告/会展/公关",
        "value": 6254
      },
      {
        "legend": "互联网/电子商务",
        "value": 5474
      },
      {
        "legend": "基金/证券/期货",
        "value": 5290
      },
      {
        "legend": "专业服务/咨询",
        "value": 4981
      },
      {
        "legend": "贸易/进出口/租赁",
        "value": 4979
      }
    ]
  }
}
```  
#### 60.职场问答首页-get：/workplaceQA/page-(\d+)/num-(\d+)/token-(\w+)  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	page		Y	string		页数
	num			Y	string		每页的数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "meet_num": 123,
      "name": "张岩",
      "expert_id": 2,
      "image": "image_img02",
      "title": "你离成为人生赢家只差一副小丁丁",
      "tag": "android",
      "like_num": 12,
      "address": "北京2"
    },
    {
      "meet_num": 123,
      "name": "张岩",
      "expert_id": 2,
      "image": "image_img02",
      "title": "你离成为人生赢家只差一副JJ",
      "tag": "android",
      "like_num": 12,
      "address": "北京2"
    }
  ]
}
```  

#### 61.职场问答首页轮播图-get：/workplaceQA-slide  
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "",
  "data": [
    {
      "image": "image_img03",
      "id": 3
    },
    {
      "image": "image_img04",
      "id": 4
    }
  ]
}
```  

#### 62.话题列表-post：/workplaceQA/topic_list  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	page		Y	string		页数
	num			Y	string		每页的数量
	field		Y	string		话题分类（简历，职业规划）
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "11",
  "data": [
    {
      "meet_num": 1,
      "name": "徐建春",
      "title": "test组团：提升人际技能，快速自我增值",
      "image": "http://images.zhaopintt.com/expert8.jpeg",
      "address": "北京 西直门",
      "tag": "职涯规划师，心理咨询师，甜心阁创始人",
      "expert_id": 8,
      "create_time": "2016-11-14T16:55:11",
      "like_num": 0,
      "topic_id": 20
    },
    {
      "meet_num": 12,
      "name": "小粉",
      "title": "职场秘籍：人格判读和沟通技巧",
      "image": "http://images.zhaopintt.com/expert7.jpeg",
      "address": "北京",
      "tag": "馒头商学院BD总监，馒头微课负责人",
      "expert_id": 7,
      "create_time": "2016-11-14T18:31:50",
      "like_num": 90,
      "topic_id": 18
    },
    {
      "meet_num": 12,
      "name": "小粉",
      "title": "如何运营好一次线上微课堂",
      "image": "http://images.zhaopintt.com/expert7.jpeg",
      "address": "北京",
      "tag": "馒头商学院BD总监，馒头微课负责人",
      "expert_id": 7,
      "create_time": "2016-11-14T18:32:02",
      "like_num": 90,
      "topic_id": 17
    }
  ]
}
```  

#### 63.专家详情页-get：/workplaceQA/expert-{expert}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	expert		Y	string		专家id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "2",
  "data": {
    "topic": [
      {
        "meet_num": 2,
        "status": null,			(该用户在本话题的状态-和预约状态相同-null=未预约过)
        "little_image": "http://tse2.mm.bing.net/th?id=OIP.Meff9c97f3dc014a82830c609b051ba6bo0&w=175&h=135&c=7&rs=1&qlt=90&o=",
        "title": "如何运营好一次线上微课堂",
        "money": "499",
        "score": "9.8",
        "id": 7
      },
      {
        "meet_num": 5,
        "status": null,
        "little_image": "http://tse1.mm.bing.net/th?&id=OIP.M9e8abd51ea9771472f25981e5eda8f89o0&w=294&h=300&c=0&pid=1.9&rs=0&",
        "title": "职场秘籍：人格判读和沟通技巧",
        "money": "600",
        "score": "9.5",
        "id": 8
      }
    ],
    "evaluate": [],
    "expert": {
      "meet_num": 12,
      "name": "小粉",
      "introduction": "去年四月加入馒头商学院，经历了馒头微课从0到1的搭建，馒头微课负责人，因为之前广泛的文化产业从业经历而成为馒头商学院首席跨界官；\n\n从2010年开始，兼职与同伴创立独立新媒体《文艺生活周刊》，时任音乐主编，带领团队驰骋在国内独立音乐圈，作为多名现在当红炸子鸡的第一篇人物专访的写作者和参加者，见证了独立音乐圈的跌宕起伏。\n\n曾经经历过国内最大规模的音乐节（当年），运营过青年文化的酷品牌。\n\n从2013年开始担任电子迷幻乐队香料的经纪人，助力乐队登上各大音乐节舞台，打造“没钱没资源的小众风格乐队如何做推广”的成功案例。\n\n跨界爱好者，给多家媒体、机构提供策划、营销、产品设计等服务。",
      "image": "http://hangjia.qiniudn.com/FjWLQMp8ougAmxR_HCEFEfQmGcK1!avatar",
      "free_time": "周末",
      "work_years": "3年以下",
      "email": "178277658@qq.com",
      "mobile": "18301656040",
      "slide": 1,
      "tag": "馒头商学院BD总监，馒头微课负责人",
      "like_num": 90,
      "is_show": 1,
      "dt_create": "2016-11-11T10:53:42",
      "address": "北京",
      "image_introduction": "http://hangjia.qiniudn.com/FnhuePT_SuIRKPjzduuJ-uW1bmCe!mainbody",
      "id": 7,
      "dt_update": "2016-11-11T10:53:42"
    }
  }
}
```  

#### 64.话题详情页-get：/workplaceQA/topic-{topic}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	topic		Y	string		话题id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "2",
  "data": {
	"is_process": 0,	(是否预约过，0=未预约，1=已预约，2=已确认，3=已付款，4=已见面)
	"is_pay": 0,		(是否支付，1=支付，0=未支付)
    "meet_num": 11,
    "big_image": "image01.png",
    "score": "0",
    "little_image": "image01.png",
    "title": "你离成为人生赢家只差一副眼镜",
    "money": "600/次",
    "id": 1,
    "evaluate_num": 0,
    "expert_id": 1,
    "create_time": "2016-07-25T15:59:16",
    "topic_time": "2016-07-25T15:59:16",
    "time_long": "1.5小时",
    "desc": "为了缓解小编们买不起棉裤的尴尬气氛，北京市城市管理委供热办相关负责人前两天表示：准备召开第二次气象会商，对7号前后的冷空气进行研制，如果在15号正常供暖前连续五天平均气温低于5℃，就有可能提前供暖。"
  }
}
```  

#### 65.对专家的评价列表-get：/workplaceQA/evaluate/page-{page}/num-{num}/expert-{expert}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	expert		Y	string		专家id
	page		Y	string		页数
	num			Y	string		每页的数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "title": "你离成为人生赢家只差一副眼镜",
      "evaluate": "精彩的内容，得体的服饰，精心打理过的发型，丽丽老师就是我向往的充满魅力的女人，丽丽老师不仅根据我的脸型",
      "create_time": "2016-07-25T15:59:16",
      "avatar": null,
      "user_name": null,
      "id": 1
    },
    {
      "title": "你离成为人生赢家只差一副眼镜",
      "evaluate": "精彩的内容，得体的服饰，精心打理过的发型，丽丽老师就是我向往的充满魅力的女人，丽丽老师不仅根据我的脸型",
      "create_time": "2016-07-25T15:59:16",
      "avatar": null,
      "user_name": null,
      "id": 2
    }
  ]
}
```  

#### 66-1.写评价页-get：/workplaceQA/evaluate?token={token}&reservation_id={reservation_id}  
参数：
		
	参数名称		必填	类型		描述
	token				Y	string		用户id	
	reservation_id		Y	string		消息id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": {
    "meet_time": "2016-11-10 11:38:45",
    "meet_address": "北京三里屯",
    "name": "徐帅楠",
    "little_image": "image01.png",
    "title": "你离成为人生赢家只差两副小丁丁"
  }
}
```  

#### 66-2.写评价页-post：/workplaceQA/evaluate  
参数：
		
	参数名称		必填	类型		描述
	token				Y	string		用户id	
	reservation_id		Y	string		消息id
	score				Y	string		评分
	evaluate			Y	string		评价
返回成功：
```{
  "status": "success",
  "msg": "评价提交成功",
  "token": "12",
  "data": {
    "errorcode": 0
  }
}
```  

#### 67.预约页-post：/workplaceQA/reservation  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	expert_id		Y	string		专家id
	topic_id		Y	string		话题id
	meet_message	Y	string		见面地点和时间，长度255
	meet_question	Y	string		约见问题

返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "11",
  "data": {
    "errorcode": 0
  }
}
```  

#### 68.付款页-post：/workplaceQA/pay  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	pay_type		Y	string		支付类型('wx'=微信，'alipay'=支付宝)
	topic_id		Y	string		话题id
返回成功：
```{
  "status": "success",
  "msg": "支付成功",
  "token": "122",
  "data": {
    "errorcode": 0,
    "charge": {
      "order_no": "be1e331ea65511e6bcce606c6604429a",
      "extra": {},
      "app": "app_eTiLm1mvTGe5O4mv",
      "livemode": false,
      "currency": "cny",
      "time_settle": null,
      "time_expire": 1478686987,
      "id": "ch_9CGeX5OC0440un1qH89Si1qP",
      "subject": "徐帅楠",
      "failure_msg": null,
      "channel": "wx",
      "metadata": {
        "topic": 1,
        "user": "122",
        "expert": 1
      },
      "body": "你离成为人生赢家只差一副眼镜",
      "credential": {
        "object": "credential",
        "wx": {
          "packageValue": "Sign=WXPay",
          "timeStamp": 1478679787,
          "sign": "0a2db199c4d4a2f552ad114870c354cb786090e0",
          "partnerId": "1276847601",
          "appId": "wxtqflkcs0mlgot0ql",
          "prepayId": "1101000000161109x5unvtpcej5ke5sy",
          "nonceStr": "9eb6820021ed25d9c1071dda1897c8df"
        }
      },
      "client_ip": "127.0.0.1",
      "description": null,
      "amount_refunded": 0,
      "refunded": false,
      "object": "charge",
      "paid": false,
      "amount_settle": 60000,
      "time_paid": null,
      "failure_code": null,
      "refunds": {
        "url": "/v1/charges/ch_9CGeX5OC0440un1qH89Si1qP/refunds",
        "has_more": false,
        "object": "list",
        "data": []
      },
      "created": 1478679787,
      "transaction_no": null,
      "amount": 60000
    }
  }
}
```  

#### 69.付款成功页-get：/workplaceQA/pay-success/message-{message_id}/token-{token}  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	message_id		Y	string		进入付款页的消息id
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": "请你于46589765\n在None\n与张岩老师见面\n联系电话：18301656040\n"
}
```

#### 70.新消息列表-get：/message/token-{token}  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": {
    "topic_message": 5,		(话题消息未读数量)
    "resume_message": 0		(简历相关消息未读数量)
  }
}
```  

#### 71.消息-话题进行中-get：/message/topic-processing/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	page		Y	string		页数
	num			Y	string		每页的数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": [
    {
      "status": "待约见",
      "name": "徐帅楠",
      "little_image": "image01.png",
      "title": "你离成为人生赢家只差一副眼镜",
      "money": "600",
      "is_read": "0",			（是否阅读，0=未读，1=已读）
      "tag": "python后台工程师",
      "is_pay": "0",				（是否支付，0=未付款，1=已付款）
	  "id": 1
    },
    {
      "status": "待同意",
      "name": "徐帅楠",
      "little_image": null,
      "title": null,
      "money": null,
      "is_read": "0",				（是否阅读，0=未读，1=已读）
      "tag": "python后台工程师",
      "is_pay": "0"				（是否支付，0=未付款，1=已付款）
	  "id": 2
    },
    {
      "status": "待付款",
      "name": "徐帅楠",
      "little_image": "image01.png",
      "title": "你离成为人生赢家只差一副JJ",
      "money": "700",
      "is_read": "0",				（是否阅读，0=未读，1=已读）
      "tag": "python后台工程师",
      "is_pay": "0"				（是否支付，0=未付款，1=已付款）
	  "id": 3
    },
    {
      "status": "待同意",
      "name": "徐帅楠",
      "little_image": "image01.png",
      "title": "你离成为人生赢家只差一副眼镜",
      "money": "600",
      "is_read": "0",				（是否阅读，0=未读，1=已读）
      "tag": "python后台工程师",
      "is_pay": "0"				（是否支付，0=未付款，1=已付款）
	  "id": 4
    }
  ]
}
```  

#### 72.消息-话题待评价-get：/message/topic-evaluated/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	page		Y	string		页数
	num			Y	string		每页的数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": [
    {
      "status": "待评价",
      "name": "徐帅楠",
      "little_image": "image01.png",
      "title": "你离成为人生赢家只差一副小丁丁",
      "money": "880",
      "is_read": "0",				（是否阅读，0=未读，1=已读）
      "tag": "python后台工程师",
      "is_pay": "1"				（是否支付，0=未付款，1=已付款）
	  "id": 5
    }
  ]
}
```  

#### 73.消息-话题已完成-get：/message/topic-finish/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	page		Y	string		页数
	num			Y	string		每页的数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": [
    {
      "status": "未同意",
      "name": "张岩",
      "little_image": "image01.png",
      "title": "你离成为人生赢家只差一副眼镜",
      "money": "600",
      "is_read": "0",			（是否阅读，0=未读，1=已读）
      "tag": "android",
      "is_pay": "1"				（是否支付，0=未付款，1=已付款）
	  "id": 6
    }
  ]
}
```  
#### 74.消息-详情-get：/message-full/message-{message_id}/token-{token}  
状态码：
		
		1-->已预约,待同意，
		2-->已确认,待付款，
		3-->已付款,待约见，
		4-->已见面,待评价，
		10-->已评价,完成，
		11-->已取消预约，
		12-->未同意，
		13-->已过期，
		14-->未见面，
		15-->已取消支付  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "12",
  "data": {
    "status": 3,					(状态码)
	"topic_id": 1，					（话题id，支付用）
    "time_line": [					（时间线，约见流程）
      {
        "info": "已预约，等待见面",
        "extra": [],
        "time": "2016-11-09 18:19:44"
      },
      {
        "info": "专家已确认，请您付款",
        "extra": [],
        "time": "2016-11-10 11:38:45"
      }
    ],
    "topic_info": {						（话题-专家-金额）
      "topic": "你离成为人生赢家只差两副小丁丁",
      "money": "300",
      "expert": "徐帅楠"
    },
    "metadata": {
      "status_info": "约会费用已支付",						（顶部文字）
      "status_little_info": "已给出联系方式，请与行家确认好约见时间和地点",		(顶部小字)
      "touch_info": {							(联系方式，仅支付成功，其他状态为{})
        "mobile": "18301656040",
        "email": "178277658@qq.com"
      }
    }
  }
}
```  

#### 75.用户自主提问-post：/workplaceQA/question  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	field			Y	string		问题所在领域
	question		Y	string		问题内容
返回成功：
```{
  "status": "success",
  "msg": "问题已提交，我们会根据你的问题尽快帮您找到合适专家。",
  "token": "12",
  "data": {
    "errorcode": 0
  }
}
```  
#### 76.取消预约、取消付款：/workplaceQA/cancel  
参数：
		
	参数名称		必填	类型		描述
	token			Y	string		用户id	
	status			Y	string		状态id（取消预约传1，取消支付传2）
	message_id		Y	string		消息id
返回成功：
```{
  "status": "success",
  "msg": "取消预约成功",
  "token": "12",
  "data": {
    "errorcode": 0
  }
}
```  
返回失败：
```{
  "status": "fail",
  "msg": "消息id有误",
  "token": "12",
  "data": {
    "errorcode": 100
  }
}
```  
