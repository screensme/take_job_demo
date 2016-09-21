###APP后端API接口文档  
OPEN API接口地址:http://xxx.xxx.xxx:8889/  
测试内网:192.168.12.146  
测试外网:182.92.99.38  
支持格式:json

##操作记录：
<div>
    <table border="0">
      <tr>
        <th>时间</th>
        <th>状态</th>
		<th>动作</th>
      </tr>
      <tr>
        <td>2016-8.21</td>
        <td>创建</td>
		<td>新建基本接口，post有可能不可用</td>
      </tr>
	<tr>
        <td>8.23</td>
        <td>修改</td>
		<td>接口连接数据库，返回的json会有变化</td>
	</tr>
	<tr>
        <td>8.24</td>
        <td>修改</td>
		<td>消息(简历状态)-待沟通-->改为-已通知;消息页和消息通知接口修改，数据变更;职位详情，url改变，需要传职位id；公司详情，url改变，需要传公司id。首页和搜索页url改变，都需要增加两个参数页数page和每页显示数量num</td>
	</tr>
	<tr>
        <td>8.25</td>
        <td>修改</td>
		<td>修改简历基本信息，所有简历状态的接口，都加了两个参数page，和num，修改简历完成，注意查看要传的数据的格式；简历编辑（实习经历）的url有变化；查看收藏，增加取消收藏</td>
	</tr>
	<tr>
        <td>8.26</td>
        <td>增-改</td>
		<td>增加接口查看收藏，收藏取消收藏，在首页和搜索，增加了字段，公司company_logo，显示职位状态(全职，兼职，实习，不限);简历投递接口完成</td>
	</tr>
	<tr>
        <td>8.27</td>
        <td>增-改</td>
		<td>增加短信验证接口；注册和忘记密码，需要多传一个参数code；修改密码接口，传的mobile改为token；搜索接口，查找职位状态job_type；修改登录返回数据</td>
	</tr>
	<tr>
        <td>8.28</td>
        <td>改</td>
		<td>简历修改基本信息和教育背景，不成功的bug；首页和搜索返回的薪资字段改变salary_start，salary_end，返回的都是多少多少K</td>
	</tr>
	<tr>
        <td>9.7-9.12</td>
        <td>增-改</td>
		<td>注册、登陆增加了umeng_id和jiguang_id。新建-公司详情的3个接口。新建修改个人头像和简历头像的两个接口</td>
	</tr>
    </table>
</div>

##url
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
xxx不用14.公司详情get：/company-full/company-{company_id}/token-{token}  
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
***
#####简历状态：  
	
	名称					状态
	'post'				发送
	'viewed'			被查看
	'pass', 'info'		简历通过
	'notify'			邀请面试(两个状态都属于面试通过)
	'deny'				不合适	

***
#####收藏状态：  
	
	名称					状态
	取消收藏				0
	已收藏/收藏成功			1
	收藏失败				2	
***
#####推送自定义返回值：  
	
	名称								状态
	系统消息(push_type)				10
	简历投递状态(push_type)			20

	被查看(push_code)				21
	待沟通(push_code)				22
	面试(push_code)					23
	不合适(push_code)				24
***
#####首页点击全职兼职： 调用接口： /search  
参数：
		
	参数名称			必填	类型			描述
	token				Y	string		用户id
	page				Y	string		页数
	num					Y	string		每页显示数量
	job_type			Y	string		全职:"fulltime",兼职/实习:['parttime','intern']
返回结果--同其他搜索结果
***
##接口介绍
####1.首页get：/home/page-{page}/num-{num}/token-{token}  
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
####2.登录post：/auth/login
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
}```  
返回成功：
```{
  "status": "success",
  "msg": "登陆成功",
  "token": 170,
  "data": {
    "user_name": "屌先生",
	"cv_name": "屌先生",	(简历中的姓名，判断是否重新填写简历用)
    "id": 170,
    "avatar": "",
    "sex": "男"
  }
}```  
####3.登出get：/auth/logout/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
返回成功：
```{
  "status": "success",
  "msg": "成功退出登录",
  "token": "123456",
  "data": {}
}```  
返回失败：
```{
  "status": "fail",
  "msg": "没有此用户!",
  "token": ""
}```  
####4.注册post：/auth/register  
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
}```  
返回失败：
```{
  "status": "fail",
  "msg": "登录手机号有误，请重新输入",
  "token": "",
  "data": {}
}```  
返回失败2：
```{
  "status": "fail",
  "msg": "手机号已经被注册",
  "token": 183,
  "data": {}
}```  
####5.修改密码post：/auth/editpwd  
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
}```  
返回失败：
```{
  "status": "fail",
  "msg": "输入的密码不能为空",
  "token": "",
  "data": {}
}```  
####6.搜索页post：/search  
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
####7.消息页get：/message/resume/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
返回成功：
```	{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": 4
}```  
####8.消息(简历状态)get(全部)：/message/resume-allstatus/page-{page}/num-{num}/token-{token}  
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
}```  
####9.消息(简历状态)get(被查看)：/message/resume-viewed/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量

####10.消息(简历状态)get(已通知)：/message/resume-communicated/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量

####11.消息(简历状态)get(面试通过)：/message/resume-passed/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量

####12.消息(简历状态)get(不合适)：/message/resume-improper/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
 
####13.职位详情get：/position-full/job-{job_id}/token-{token}
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
}```  
####14.公司详情get：/company-full/company-{company_id}/token-{token}
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
}```  
####15.个人信息页get(基本信息)：/me/token-{token}  
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
}```  
####16.简历查看get：/resume-view/token-{token}
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
}```  
####17.简历编辑-基本信息post：/resume-edit-basic  
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
    }```  
返回成功：
```{
    "status":"success",
    "msg":"",
    "token":"177",
    "data":167
}```  
####18.简历编辑-教育经历post：/resume-edit-education  
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
```{"status": "success", "msg": "", "token": "177", "data": 167}```  
####19.简历编辑-职业意向post：/resume-edit-expect  
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
    }```  
返回成功：
```{"status": "success", "msg": "", "token": "177", "data": 167}```  
####20.简历编辑-实习经历post：/resume-edit-career  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	career		Y	string		用户的实习经历，注意格式如下
<font color=blue>（career本身是list格式，将这个list转换为string格式传过来）如下</font>
```[
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
]```  
返回成功：
```{"status": "success", "msg": "", "token": "177", "data": 167}```  
####21.简历编辑-自我评价post：/resume-edit-evaluation  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	description	Y	string		用户的自我评价
返回成功：
```{"status": "success", "msg": "", "token": "177", "data": 167}```  
####22.意见反馈post：/feedback  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
	info		Y	string		反馈的消息内容
	email		N	string		反馈用户的邮箱（选填）
返回成功：
```{
  "status": "success",
  "msg": "反馈成功",
  "token": "111",
  "data": {
    "errorcode": 0
  }
}```  
返回失败：
```{
  "status": "fail",
  "msg": "请输入反馈的内容",
  "token": "",
  "data": {
    "errorcode": 1000
  }
}```
####23.查看收藏get：/view_collect/page-{page}/num-{num}/token-{token}  
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
}```  
####24.增加和删除收藏post：/add_or_del_collect  
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
}```  
返回取消收藏成功：
```{
  "status": "success",
  "msg": "已取消收藏",
  "token": "1",
  "data": 1
}```  
####25.热门搜索职位列表get：/hot_job/token-{token}
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
}```  
####26.热门搜索城市列表get：/hot_city/token-{token}  
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
}```  
####27.简历投递post：/post-resume  
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
}```  
返回失败：
```{
  "status": "fail",
  "msg": "已投递的职位",
  "token": "1",
  "data": {
	'errorcode':10
	}
}```  
####28.忘记，找回密码post：/auth/forgetpwd  
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
}```  
返回失败：  
```{
  "status": "fail",
  "msg": "验证码超时，请重新获取",
  "token": "",
  "data": {
    "token": ""
  }
}```  
####29.短信发送接口post：/sendsms  
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
}```  
返回失败：  
```{
  "status": "fail",
  "msg": "短信发送失败",
  "token": "",
  "data": {}}```  
####30.推荐职位post：/recommend-job  
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
}```
####31.消息详情get：/message-full/job-{job_id}/token-{token}  
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
}```  
####32.修改个人信息post：/user-info/edit  
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
}```  
####33.修改个人头像post：/user-info/avatar  
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
}```  
####34.修改简历头像post：/resume-edit-avatar  
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
}```  
####35.公司详情-公司信息get：/company-full/info/company-{company_id}/token-{token}  
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
}```  
返回错误:
```{
  "status": "fail",
  "msg": "没有公司详情!",
  "token": "1",
  "data": {
    "errorcode": 1001
  }
}```  
####36.公司详情-企业详情get(公司介绍，大事记)：/company-full/company/company-{company_id}/token-{token}  
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
}```  
返回错误:
```{
  "status": "fail",
  "msg": "没有公司详情!",
  "token": "1",
  "data": {
    "errorcode": 1001
  }
}```  
####37.公司详情-所有职位post：/company-full/job  
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
}```  
返回错误:
```{
  "status": "fail",
  "msg": "没有公司详情!",
  "token": "1",
  "data": {
    "errorcode": 1001
  }
}```  
####38.急速招聘post：/speed-job   
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
}```  
返回失败：
```{
  "status": "fail",
  "msg": "",
  "token": "123",
  "data": []
```
####39.搜索公司名post：/search-company  
		
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
}```  
####40.获取版本,自动更新post（仅Android）：/get-version  
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
    "isupdate": 1		（1表示需要更新，0表示不需要更新）
  }
}```  
返回失败：
```{
  "status": "fail",
  "msg": "非安卓手机",
  "token": "",
  "data": {
    "errorcode": 1000,
    "update_url": "",
    "isupdate": 0
  }
}```