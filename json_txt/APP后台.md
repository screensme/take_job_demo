###APP后端API接口文档  
OPEN API接口地址:http://xxx.xxx.xxx:8889/  
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
		<td>我</td>
	</tr>
    </table>
</div>

##url
1.首页get：/home/token-{token}  
2.登录post：/auth/login  
3.登出get：/auth/logout/token-{token}  
4.注册post：/auth/register  
5.修改密码post：/auth/editpwd  
6.搜索页post：/search  
7.消息页get：/message/resume/token-{token}  
8.简历状态get(全部)：/message/resume-allstatus/token-{token}  
9.简历状态get(被查看)：/message/resume-viewed/token-{token}  
10.简历状态get(待沟通)：/message/resume-communicated/token-{token}  
11.简历状态get(面试通过)：/message/resume-passed/token-{token}  
12.简历状态get(不合适)：/message/resume-improper/token-{token}  
13.职位详情get：/position-full/token-{token}  
14.公司详情get：/company-full/token-{token}    
15.个人信息页get(基本信息)：/me/token-{token}  
16.简历查看get：/resume-view/token-{token}  
17.简历编辑-基本信息post：/resume-edit-basic  
18.简历编辑-教育经历post：/resume-edit-education  
19.简历编辑-职业意向post：/resume-edit-expect  
20.简历编辑-实习经历post：/resume-edit-experience  
21.简历编辑-项目实践post：/resume-edit-item  
22.简历编辑-自我评价post：/resume-edit-evaluation  
23.意见反馈post：/feedback

##接口介绍
####1.首页get：/home/token-{token}  
参数：
		
	参数名称	必填	类型		描述
	token	  必填	  string	用户id
返回结果：
```
{
  "status": "success",
  "msg": "",
  "token": "111",
  "data": [
    {
      "company_station": "公司状态（合资、民营、国企）",
      "money": "薪资",
      "image": "公司logo",
      "company_type": "公司类型（游戏、互联网、硬件）",
      "seniority": "工龄",
      "education": "学历",
      "job_id": "职位id",
      "company_scale": "公司规模",
      "company_name": "公司名称",
      "company_address": "公司地址",
      "release_time": "发布时间",
      "job_name": "职位名称"
    },
    {
      "company_station": "公司状态（合资、民营、国企）2",
      "money": "薪资2",
      "image": "公司logo2",
      "company_type": "公司类型（游戏、互联网、硬件）2",
      "seniority": "工龄2",
      "education": "学历2",
      "job_id": "职位id2",
      "company_scale": "公司规模2",
      "company_name": "公司名称2",
      "company_address": "公司地址2",
      "release_time": "发布时间2",
      "job_name": "职位名称2"
    },
    {
      "company_station": "公司状态（合资、民营、国企）3",
      "money": "薪资3",
      "image": "公司logo3",
      "company_type": "公司类型（游戏、互联网、硬件）3",
      "seniority": "工龄3",
      "education": "学历3",
      "job_id": "职位id3",
      "company_scale": "公司规模3",
      "company_name": "公司名称3",
      "company_address": "公司地址3",
      "release_time": "发布时间3",
      "job_name": "职位名称3"
    }
  ]
}```
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
  "token": "8626fa72-4275-11e6-92c4-c81f664404a0",
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
返回成功：
```{
  "status": "sucess",
  "msg": "",
  "token": "123123",
  "data": {
    "mobile": "13333333333",
    "image": "http://7xlo2h.com1.z0.glb.clouddn.com/avatar/default_avatar.png",
    "pwd": "111111",
    "uuid": "123123"
  }
}```  
返回失败：
```{
  "status": "fail",
  "msg": "登录手机号有误，请重新输入",
  "token": "",
  "data": {}
}``` 
####5.修改密码post：/auth/editpwd  
####6.搜索页post：/search
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
####8.简历状态get(全部)：/message/resume-allstatus/token-{token} 
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "job_id": "职位id",
      "company_address": "公司地址(只城市)",
      "money": "薪资",
      "image": "公司logo",
      "resume_status": "viewed",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称",
      "company_name": "公司名称"
    },
    {
      "job_id": "职位id2",
      "company_address": "公司地址(只城市)2",
      "money": "薪资2",
      "image": "公司logo2",
      "resume_status": "communicated",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称2",
      "company_name": "公司名称2"
    },
    {
      "job_id": "职位id3",
      "company_address": "公司地址(只城市)3",
      "money": "薪资3",
      "image": "公司logo3",
      "resume_status": "passed",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称3",
      "company_name": "公司名称3"
    },
    {
      "job_id": "职位id4",
      "company_address": "公司地址(只城市)4",
      "money": "薪资4",
      "image": "公司logo4",
      "resume_status": "improper",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称4",
      "company_name": "公司名称4"
    }
  ]
}```  
####9.简历状态get(被查看)：/message/resume-viewed/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "job_id": "职位id",
      "company_address": "公司地址(只城市)",
      "money": "薪资",
      "image": "公司logo",
      "resume_status": "viewed",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称",
      "company_name": "公司名称"
    }
  ]
}```  
####10.简历状态get(待沟通)：/message/resume-communicated/token-{token} 
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "job_id": "职位id2",
      "company_address": "公司地址(只城市)2",
      "money": "薪资2",
      "image": "公司logo2",
      "resume_status": "communicated",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称2",
      "company_name": "公司名称2"
    }
  ]
}```  
####11.简历状态get(面试通过)：/message/resume-passed/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "job_id": "职位id3",
      "company_address": "公司地址(只城市)3",
      "money": "薪资3",
      "image": "公司logo3",
      "resume_status": "passed",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称3",
      "company_name": "公司名称3"
    }
  ]
}```  
####12.简历状态get(不合适)：/message/resume-improper/token-{token} 
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": [
    {
      "job_id": "职位id4",
      "company_address": "公司地址(只城市)4",
      "money": "薪资4",
      "image": "公司logo4",
      "resume_status": "improper",
      "feedback": "2016-04-26 16:33:19",
      "job_name": "职位名称4",
      "company_name": "公司名称4"
    }
  ]
}```  
####13.职位详情get：/position-full/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": {
    "company_info": {
      "company_station": "公司状态（合资、民营、国企）",
      "image": "公司logo",
      "company_type": "公司类型（游戏、互联网、硬件）",
      "authenticate": "公司是否认证",
      "company_name": "公司名称",
      "company_scale": "公司规模"
    },
    "money": "薪资",
    "address": "公司地址",
    "job_type": "职位类型（全职、兼职）",
    "full_address": "详细地址",
    "welfare": "职位福利（饭补、美女多、20薪）",
    "seniority": "工龄",
    "education": "学历",
    "job_desc": "职位详情",
    "company_id": "公司id",
    "company_address": "公司地址(只城市)",
    "job_name": "职位名称"
  }
}```  
####14.公司详情get：/company-full/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
返回成功：
```{
  "status": "success",
  "msg": "",
  "token": "123",
  "data": {
    "company_scale": "公司规模",
    "company_station": "公司状态（合资、民营、国企）",
    "company_name": "公司名称",
    "company_address": "公司地址(只城市)",
    "job_list": [
      {
        "release_time": "发布时间",
        "company_station": "公司状态（合资、民营、国企）",
        "job_id": "职位id1",
        "money": "薪资",
        "seniority": "工龄",
        "education": "学历",
        "company_type": "公司类型（游戏-互联网-硬件）",
        "address": "公司地址",
        "company_scale": "公司规模"
      },
      {
        "release_time": "发布时间2",
        "company_station": "公司状态（合资、民营、国企）2",
        "job_id": "职位id2",
        "money": "薪资2",
        "seniority": "工龄2",
        "education": "学历2",
        "company_type": "公司类型（游戏-互联网-硬件）2",
        "address": "公司地址2",
        "company_scale": "公司规模2"
      },
      {
        "release_time": "发布时间3",
        "company_station": "公司状态（合资、民营、国企）3",
        "job_id": "职位id3",
        "money": "薪资3",
        "seniority": "工龄3",
        "education": "学历3",
        "company_type": "公司类型（游戏-互联网-硬件）3",
        "address": "公司地址3",
        "company_scale": "公司规模3"
      }
    ],
    "image": "公司logo",
    "company_type": "公司类型（游戏-互联网-硬件）",
    "company_desc": "公司介绍"
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
    "user_image": "头像",
    "sex": "性别",
    "polity_face": "政治面貌",
    "education": "学历",
    "user_id": "个人id",
    "name": "用户名",
    "mobile": "手机号",
    "token": "登陆用户id",
    "marriage": "婚姻",
    "place": "现居住地",
    "email": "邮箱",
    "birth_year": "出生年月"
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
  "token": "23",
  "data": {
    "experience": {
      "job_duty": "工作职责",
      "gs_trade": "公司行业",
      "gs": "公司名称",
      "start_year2": "开始时间年",
      "end_year2": "结束时间月",
      "gs_job": "职位名称",
      "gs_address": "工作地点",
      "start_month2": "开始时间月"
    },
    "item": {
      "start_year3": "开始时间年",
      "item_des": "项目描述",
      "item_name": "项目名称",
      "item_duty": "职位名称",
      "end_month3": "结束时间月",
      "end_year3": "结束时间年",
      "start_month3": "开始时间月"
    },
    "expect": {
      "expect_salary": "期望薪资",
      "expect_trade": "期望行业",
      "work_state": "求职意向，是否全职",
      "expect_city": "期望地点",
      "expect_job": "期望职位"
    },
    "basic": {
      "user_image": "头像",
      "sex": "性别",
      "polity_face": "政治面貌",
      "education": "学历",
      "name": "用户名",
      "user_id": "个人id",
      "uuid": "id111",
      "mobile": "手机号",
      "marriage": "婚姻",
      "place": "现居住地",
      "email": "邮箱",
      "birth_year": "出生年月"
    },
    "education": {
      "start_month": "开始时间月",
      "start_year": "开始时间年",
      "end_year": "毕业时间年",
      "school": "学校名称",
      "education2": "学历",
      "end_month": "毕业时间月",
      "major": "专业"
    },
    "evaluation": "自我评价"
  }
}```
####17.简历编辑-基本信息post：/resume-edit-basic 
####18.简历编辑-教育经历post：/resume-edit-education 
####19.简历编辑-职业意向post：/resume-edit-expect 
####20.简历编辑-实习经历post：/resume-edit-experience
####21.简历编辑-项目实践post：/resume-edit-item
####22.简历编辑-自我评价post：/resume-edit-evaluation 
####23.意见反馈post：/feedback



