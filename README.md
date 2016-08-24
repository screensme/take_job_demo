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
        <td>2016-8-23</td>
        <td>修改</td>
		<td>接口连接数据库，返回的json会有变化</td>
	</tr>
	<tr>
        <td>2016-8-24</td>
        <td>修改</td>
		<td>消息(简历状态)-待沟通-->改为-已通知</td>
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
10.简历状态get(已通知)：/message/resume-communicated/token-{token}  
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
每页显示10个（忘了写成动态的了，之后再改）
参数：
		
	参数名称	必填	类型		描述
	token	  Y	  string	用户id
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
      "scale_str": "1000-5000人",
      "trade": "",
      "job_city": "北京",
      "company_name": "文新教育集团",
      "boon": "五险一金,补充保险,年奖季奖",
      "education_str": "不限",
      "job_name": "测试职位",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:15:38"
    },
    {
      "salary_str": "6000-7000",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "北京",
      "company_name": "归途如虹",
      "boon": "五险一金,餐饮补助,通讯补贴,弹性工作",
      "education_str": "硕士",
      "job_name": "市场经理",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T18:55:29"
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
      "salary_str": "12000-15000",
      "scale_str": "1000-5000人",
      "trade": "",
      "job_city": "北京",
      "company_name": "文新教育集团",
      "boon": "五险一金",
      "education_str": "不限",
      "job_name": "rust",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:04:26"
    },
    {
      "salary_str": "7000-9000",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "上海",
      "company_name": "归途如虹",
      "boon": "五险一金,补充保险,年奖季奖,弹性工作,通讯补贴,餐饮补助,员工旅游",
      "education_str": "本科",
      "job_name": "后端工程师",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T18:59:04"
    },
    {
      "salary_str": "7000-12000",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "北京",
      "company_name": "归途如虹",
      "boon": "五险一金",
      "education_str": "不限",
      "job_name": "g4g",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:02:41"
    },
    {
      "salary_str": "12000-13000",
      "scale_str": "20人以下",
      "trade": "媒体/出版/文化传播",
      "job_city": "北京",
      "company_name": "wakaka",
      "boon": "五险一金,餐饮补助,通讯补贴,补充保险",
      "education_str": "不限",
      "job_name": "hhh",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:33:41"
    },
    {
      "salary_str": "9000-11000",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "北京",
      "company_name": "归途如虹",
      "boon": "五险一金,补充保险,年奖季奖,绩效奖金",
      "education_str": "不限",
      "job_name": "发单员",
      "work_years_str": "不限",
      "dt_update": "2016-08-19T19:50:16"
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
参数：
		
	参数名称	必填	类型		描述
	mobile		Y	string		手机号
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
每页显示10个（忘了写成动态的了，之后再改）  
参数：(可传很多参数，根据参数查询，至少写一个条件)
		
	参数名称	必填	类型		描述
	token	  Y	  string	用户id
	job_name	N	string		职位名称
	trade		N	string		行业
	work_years_start(0)	N	string	工作年限
	Work_year_end(50)	N	string	工作年限
	job_city(全国)	N	string	城市
	area		N	string		区域
	education_str	N	string	教育背景
	scale_start(0)	N	string	企业规模
	Scale_end(20000)	N	string	企业规模
	company_type(0)	N	string 	企业性质
	salary_start(0)	N	string	薪资范围
	Salary_end(200000)	N	string	薪资范围
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
      "salary_str": "8000-9999/月",
      "scale_str": "50-150人",
      "trade": "农/林/牧/渔,快速消费品(食品、饮料、化妆品)",
      "job_city": "北京-昌平区",
      "company_name": "北京中特聚品农业科技有限公司",
      "boon": "",
      "education_str": "中专",
      "job_name": "软件工程师/PHP工程师",
      "work_years_str": "",
      "dt_update": "2016-04-26T00:00:00"
    },
    {
      "salary_str": "8000-9999/月",
      "scale_str": "150-500人",
      "trade": "互联网/电子商务,计算机软件",
      "job_city": "北京",
      "company_name": "指点无限（北京）科技有限公司",
      "boon": "五险一金,定期体检,年终奖金,通讯补贴,绩效奖金",
      "education_str": "大专",
      "job_name": "php高级软件工程师 (职位编号：15)",
      "work_years_str": "1年经验",
      "dt_update": "2016-04-26T00:00:00"
    },
    {
      "salary_str": "10000-50000",
      "scale_str": "10000人以上",
      "trade": "网络游戏/动漫",
      "job_city": "北京",
      "company_name": "郭路路的公司",
      "boon": "年奖季奖,补充保险,年奖季奖",
      "education_str": "中专",
      "job_name": "php大牛1",
      "work_years_str": "不限",
      "dt_update": "2016-08-17T10:59:51"
    },
    {
      "salary_str": "2000-3000",
      "scale_str": "20-99人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "北京",
      "company_name": "CCC_&lt;script&gt;",
      "boon": "五险一金,补充保险,节日福利",
      "education_str": "本科",
      "job_name": "测试职位PHP",
      "work_years_str": "不限",
      "dt_update": "2016-07-25T14:58:07"
    },
    {
      "salary_str": "0-0",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "上海",
      "company_name": "归途如虹",
      "boon": "五险一金",
      "education_str": "不限",
      "job_name": "php",
      "work_years_str": "不限",
      "dt_update": "2016-08-17T18:11:27"
    },
    {
      "salary_str": "5000-6000",
      "scale_str": "500-999人",
      "trade": "移动互联网/O2O/数据服务",
      "job_city": "北京",
      "company_name": "归途如虹",
      "boon": "补充保险,年奖季奖",
      "education_str": "大专",
      "job_name": "php",
      "work_years_str": "不限",
      "dt_update": "2016-08-17T18:11:25"
    },
    {
      "salary_str": null,
      "scale_str": "250",
      "trade": null,
      "job_city": "深圳",
      "company_name": "八九八创新空间（北京）科技有限公司",
      "boon": null,
      "education_str": null,
      "job_name": "php",
      "work_years_str": "1 - 1年",
      "dt_update": "2016-08-16T00:00:00"
    },
    {
      "salary_str": null,
      "scale_str": "100",
      "trade": null,
      "job_city": "深圳",
      "company_name": "八九八创新空间（北京）科技有限公司",
      "boon": null,
      "education_str": null,
      "job_name": "php",
      "work_years_str": "1 - 1年",
      "dt_update": "2016-08-16T00:00:00"
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
####8.消息(简历状态)get(全部)：/message/resume-allstatus/token-{token} 
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
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
####9.消息(简历状态)get(被查看)：/message/resume-viewed/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
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
####10.消息(简历状态)get(已通知)：/message/resume-communicated/token-{token} 
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
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
####11.消息(简历状态)get(面试通过)：/message/resume-passed/token-{token}
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
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
####12.消息(简历状态)get(不合适)：/message/resume-improper/token-{token} 
参数：
		
	参数名称	必填	类型		描述
	token		Y	string		用户id	
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



