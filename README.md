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
        <td>2016-8-21</td>
        <td>创建</td>
		<td>新建基本接口，post有可能不可用</td>
      </tr>
	<tr>
        <td>2016-8-23</td>
        <td>修改</td>
		<td>接口连接数据库，返回的json会有变化</td>
	</tr>
	<tr>
        <td>2016-8-24</td>
        <td>修改</td>
		<td>消息(简历状态)-待沟通-->改为-已通知;消息页和消息通知接口修改，数据变更;职位详情，url改变，需要传职位id；公司详情，url改变，需要传公司id。首页和搜索页url改变，都需要增加两个参数页数page和每页显示数量num</td>
	</tr>
	<tr>
        <td>2016-8-25</td>
        <td>修改</td>
		<td>修改简历基本信息，所有简历状态的接口，都加了两个参数page，和num，修改简历完成，注意查看要传的数据的格式；简历编辑（实习经历）的url有变化；查看收藏，增加取消收藏</td>
	</tr>
	<tr>
        <td>2016-8-26</td>
        <td>增-改</td>
		<td>增加接口查看收藏，收藏取消收藏，在首页和搜索，增加了字段，公司company_logo，显示职位状态(全职，兼职，实习，不限);简历投递接口完成</td>
	</tr>
	<tr>
        <td>2016-8-27</td>
        <td>增-改</td>
		<td>增加短信验证接口；注册和忘记密码，需要多传一个参数code；修改密码接口，传的mobile改为token；搜索接口，查找职位状态job_type</td>
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

##接口介绍
####1.首页get：/home/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
返回结果：
```
{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "salary_str": "6000-7999/月",
      "scale_str": "500-1000人",
      "trade": "教育/培训/院校",
      "job_city": "北京",
      "company_name": "文新教育集团",
      "boon": "员工旅游,专业培训,绩效奖金,年终奖金",
      "education_str": "中专",
      "job_name": "课程顾问/咨询师/咨询顾问（北京就近分配）",
      "work_years_str": "1年经验",
      "dt_update": "2016-08-19T19:04:29"
    },
    {
      "salary_str": "11000-12000",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "北京",
      "company_name": "归途如虹",
      "boon": "五险一金,餐饮补助",
      "education_str": "本科",
      "job_name": "前端工程师",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T18:56:53"
    },
    {
      "salary_str": "11000-14000",
      "scale_str": "20人以下",
      "trade": "互联网/电子商务",
      "job_city": "北京",
      "company_name": "测试",
      "boon": "五险一金,补充保险,年奖季奖",
      "education_str": "不限",
      "job_name": "php",
      "work_years_str": "不限",
      "dt_update": "2016-08-23T13:08:37"
    }
  ]
}
```  
####2.登录post：/auth/login
参数：
		
	参数名称	必填	类型		描述
	mobile		Y	string		手机号
	pwd			Y	string		密码
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
  "msg": "",
  "token": "120",
  "data": {
    "mobile": "13333333333",
    "pwd": "111111",
    "uuid": "8626fa72-4275-11e6-92c4-c81f664404a0",
    "image": "http://images.huoban.io/th_21111.jpg"
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
	Work_year_end(50)	N	string		工作年限
	job_city(全国)		N	string		城市
	area				N	string		区域
	education			N	string		'不限': None,'中专': 2,'大专': 3,'本科': 4,'硕士': 5,'博士': 6
	scale_start(0)		N	string		企业规模
	Scale_end(20000)	N	string		企业规模
	company_type(0)		N	string 		企业性质
	salary_start(0)		N	string		薪资范围
	Salary_end(200000)	N	string		薪资范围
返回结果：
```
{
  "status": "success",
  "msg": "",
  "token": "1111",
  "data": [
    {
      "salary_str": "10000-14999/月",
      "scale_str": "少于50人",
      "trade": "计算机软件",
      "job_city": "北京-西城区",
      "company_name": "冷蜘蛛供应链管理（北京）有限公司",
      "boon": "五险一金,餐饮补贴,年终奖金,交通补贴",
      "education_str": "大专",
      "job_name": "PHP软件工程师",
      "work_years_str": "3-4年经验",
      "dt_update": "2016-04-26T00:00:00"
    },
    {
      "salary_str": "11000-13000",
      "scale_str": "少于50人",
      "trade": "",
      "job_city": "北京",
      "company_name": "八九八创新空间（北京）科技有限公司",
      "boon": "五险一金,补充保险,年奖季奖",
      "education_str": "本科",
      "job_name": "php",
      "work_years_str": "不限",
      "dt_update": "2016-08-16T17:38:01"
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
  "token": "22",
  "data": [
    {
      "salary_str": "面议",
      "scale_str": "20-99人",
      "job_id": 1764,
      "post_status": "allow",
      "company_type": "民营",
      "job_city": "北京",
      "company_name": "北京宠知道科技有限公司",
      "boon": "年底双薪,绩效奖金,年终分红,股票期权,弹性工作,补充医疗保险,定期体检,员工旅游",
      "education_str": "本科",
      "job_name": "产品经理",
      "work_years_str": "1-3年"
    },
    {
      "salary_str": "面议",
      "scale_str": "100-499人",
      "job_id": 27872,
      "post_status": "allow",
      "company_type": "上市公司",
      "job_city": "北京",
      "company_name": "嘉网股份",
      "boon": "",
      "education_str": "本科",
      "job_name": "C#软件工程师",
      "work_years_str": "1-3年"
    }
  ]
}```  
####9.消息(简历状态)get(被查看)：/message/resume-viewed/page-{page}/num-{num}/token-{token}  
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
      "salary_str": "0-0",
      "scale_str": "20-99人",
      "job_id": 214400,
      "post_status": "allow",
      "company_type": "民营企业/私营公司",
      "job_city": "北京",
      "company_name": "联创锐峰科技有限公司",
      "boon": "",
      "education_str": "大专",
      "job_name": "策划专员",
      "work_years_str": "不限"
    }
  ]
}```  
####10.消息(简历状态)get(已通知)：/message/resume-communicated/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "22",
  "data": [
    {
      "salary_str": "15564-1968498",
      "scale_str": "20-99人",
      "job_id": 214116,
      "post_status": "allow",
      "company_type": "国有企业",
      "job_city": "上海",
      "company_name": "归途如虹",
      "boon": "周末双休",
      "education_str": "中专",
      "job_name": "..111",
      "work_years_str": "不限"
    }
  ]
}```  
####11.消息(简历状态)get(面试通过)：/message/resume-passed/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "19",
  "data": [
    {
      "salary_str": "15564-1968498",
      "scale_str": "20-99人",
      "job_id": 214116,
      "post_status": "allow",
      "company_type": "国有企业",
      "job_city": "上海",
      "company_name": "归途如虹",
      "boon": "周末双休",
      "education_str": "中专",
      "job_name": "..111",
      "work_years_str": "不限"
    }
  ]
}```  
####12.消息(简历状态)get(不合适)：/message/resume-improper/page-{page}/num-{num}/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "68",
  "data": [
    {
      "salary_str": "0-0",
      "scale_str": "20-99人",
      "job_id": 214404,
      "post_status": "allow",
      "company_type": "民营企业/私营公司",
      "job_city": "北京",
      "company_name": "联创锐峰科技有限公司",
      "boon": "",
      "education_str": "不限",
      "job_name": "双11发单员",
      "work_years_str": "不限"
    },
    {
      "salary_str": "0-0",
      "scale_str": "20-99人",
      "job_id": 214405,
      "post_status": "allow",
      "company_type": "民营企业/私营公司",
      "job_city": "北京",
      "company_name": "联创锐峰科技有限公司",
      "boon": "",
      "education_str": "不限",
      "job_name": "国贸发单员",
      "work_years_str": "不限"
    }
  ]
}```  
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
    "salary_str": "10001-15000元/月",
    "site_name": "智联招聘",
    "company_type": "民营",
    "need_num": 5,
    "position_des": "只要您足够的优秀，这里有最好的平台、最高的课时费（打造高端教育品牌），选择大于努力！ 岗位职责： 1. 负责对本学科的学员进行“一对一或班课”教学辅导； 2. 一对一教师要根据每个学生学习以及性格的特点，制定适合的个性化学习计划和方案； 3. 班课教师要按照班课体系规定及要求完成每次授课，并做好课程记录，针对学生问题制定改进方案； 4. 与家长、学员和校区同事进行充分沟通，全方面了解学生学习及其他情况，有针对性教学，提高家长满意度； 5. 根据学生学习进度及内容，定期进行知识检测，并有针对性帮助孩子推荐其它科目的学习。 任职要求： 1. 认同洪伟教育发展目标（打造教育界精品班课和高端一对一）； 2. 具备耐心、细心和责任心，分析总结及规划能力，观察能力强； 3. 普通话标准，声音洪亮，语言表达能力强； 4. 具备较强的亲和力和幽默感，上课生动活泼； 5. 学生时代有竞赛获奖经历者或获得中高考状元者优先；",
    "local_company_id": 0,
    "work_years_start": -3,
    "major_des": "高中教师",
    "id": 222,
    "salary_type": "public",
    "salary_avg": 12500,
    "scale": 100,
    "school_str": null,
    "company_id": 0,
    "post_url": "http://jobs.zhaopin.com/394228816250174.htm",
    "company_name": "北京洪伟创新教育科技有限公司",
    "boon": "年底双薪,绩效奖金,全勤奖,交通补助,通讯补贴,带薪年假,高温补贴,节日福利",
    "education_str": "不限",
    "contact_phone": null,
    "job_name": "化学教师（初高中班课，课时费高于同行业）",
    "dt_update": "2016-04-26T00:00:00",
    "status": "open",
    "scale_str": "100-499人",
    "salary_end": 15000,
    "job_type": "fulltime",
    "job_city": "北京",
    "salary_start": 10001,
    "contact_email": null,
    "work_years_str": "不限",
    "address": null,
    "trade": "教育/培训/院校",
    "dt_origin": "2016-04-26T00:00:00",
    "work_years_end": -3,
    "major_str": null,
    "local_job_id": 0,
    "contact": null,
    "dt_create": "2016-04-26T16:33:42",
    "priority": 0
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
    "company_contact": null,
    "company_name": "北京汇能精电科技股份有限公司",
    "dt_create": "2016-03-29T10:44:19",
    "address": "北京市昌平区何营路8号企业墅18号楼",
    "company_trade": null,
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
]```  
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
返回成功：
```{"status": "success", "msg": "", "token": "177", "data": 167}```  
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
      "status": "favorite",
      "scale_str": "100-499人",
      "company_type": "合资",
      "userid": 1,
      "jobid": 3,
      "job_city": "北京",
      "job_type": "fulltime",
      "m1": "6001-8000元/月",
      "company_name": "北京领创鑫业商贸有限公司",
      "boon": "五险一金,年底双薪,交通补助,房补,全勤奖,带薪年假,节日福利,员工旅游",
      "collection_id": 378,
      "trade": "贸易/进出口",
      "job_name": "财务助理\\会计专员   （月薪8000、朝九晚六、周末双休）",
      "work_years_str": "不限"
    },
    {
      "status": "favorite",
      "scale_str": "100-499人",
      "company_type": "民营",
      "userid": 1,
      "jobid": 23,
      "job_city": "北京",
      "job_type": "fulltime",
      "m1": "4001-6000元/月",
      "company_name": "上海交大昂立国际教育北京首都机场分校",
      "boon": "五险一金,绩效奖金,包吃,包住,带薪年假,员工旅游,节日福利,加班补助",
      "collection_id": 377,
      "trade": "教育/培训/院校",
      "job_name": "课程顾问",
      "work_years_str": "不限"
    },
    {
      "status": "favorite",
      "scale_str": "",
      "company_type": "国企",
      "userid": 1,
      "jobid": 163742,
      "job_city": "北京",
      "job_type": "unclear",
      "m1": "2000-2999/月",
      "company_name": "四川长虹电器股份有限公司",
      "boon": "",
      "collection_id": 1,
      "trade": "家具/家电/玩具/礼品",
      "job_name": "客户经理",
      "work_years_str": "应届毕业生经验"
    }
  ]
}```  
####24.增加收藏post：/add_collect
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
  "data": {}
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
  "data": {}
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