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
		<td>消息(简历状态)-待沟通-->改为-已通知;消息页和消息通知接口修改，数据变更;职位详情，url改变，需要传职位id；公司详情，url改变，需要传公司id。首页和搜索页url改变，都需要增加两个参数页数page和每页显示数量num</td>
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
8.简历状态get(全部)：/message/resume-allstatus/token-{token}  
9.简历状态get(被查看)：/message/resume-viewed/token-{token}  
10.简历状态get(已通知)：/message/resume-communicated/token-{token}  
11.简历状态get(面试通过)：/message/resume-passed/token-{token}  
12.简历状态get(不合适)：/message/resume-improper/token-{token}  
13.职位详情get：/position-full/job-{job_id}/token-{token}  
14.公司详情get：/company-full/company-{company_id}/token-{token}    
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
返回成功：
```{
  "status": "sucess",
  "msg": "",
  "token": "123",
  "data": {
    "authenticated": 1,
    "post_status": "allow",
    "phonenum": "15801616013",
    "tag": "test",
    "dt_update": "2016-08-18T18:44:31",
    "dt_create": "2016-08-18T18:44:31",
    "active": 1,
    "password": "$2b$12$MK8CVHw3nfGEyqup.vCe2OUu06E/go9paz4HNGr8qTbkh1klxhGbW",
    "user_uuid": "be747a98-6530-11e6-8327-a41f72641111",
    "id": 170
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
	token		Y	string		用户id
	page		Y	string		页数
	num			Y	string		每页显示数量
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
    "position_des": "只要您足够的优秀，这里有最好的平台、最高的课时费（打造高端教育品牌），选择大于努力！ 岗位职责： 1. 负责对本学科的学员进行“一对一或班课”教学辅导； 2. 一对一教师要根据每个学生学习以及性格的特点，制定适合的个性化学习计划和方案； 3. 班课教师要按照班课体系规定及要求完成每次授课，并做好课程记录，针对学生问题制定改进方案； 4. 与家长、学员和校区同事进行充分沟通，全方面了解学生学习及其他情况，有针对性教学，提高家长满意度； 5. 根据学生学习进度及内容，定期进行知识检测，并有针对性帮助孩子推荐其它科目的学习。 任职要求： 1. 认同洪伟教育发展目标（打造教育界精品班课和高端一对一）； 2. 具备耐心、细心和责任心，分析总结及规划能力，观察能力强； 3. 普通话标准，声音洪亮，语言表达能力强； 4. 具备较强的亲和力和幽默感，上课生动活泼； 5. 学生时代有竞赛获奖经历者或获得中高考状元者优先； 6. 有班课教学经验者优先； 联系人：刘老师：13366016594（优秀老师可直接电话交流） 加入我们，您将拥有： 1. 优越的薪酬制度 行业内具有竞争优势的薪酬激励； 2. 快速的成长通道 教学能力优秀者可以加入单位，共同发展。 3. 良好的办公环境及高素质的合作团队，人性化的企业管理理念。 工作地址： 北京市西城区西直门南小街国英大厦6楼6E 查看职位地图 北京洪伟创新教育科技有限公司 该公司其他职位 洪伟教育是专门致力于中小学学生成绩提高、学习能力开发和培养、及全方位分析学生心理和家庭教育的课外辅导机构。成立四年来本着“一切为了学生”的办学宗旨，培养了数千名优秀学子，倾力打造独具洪伟教育特色的中小学系统强化提高平台。长期以来的不断努力聚集了一批教育界精英和北京各大名校的优秀一线教师，以优质的教学服务理念与雄厚的师资力量相结合，从而使广大学员考上了自己理想的学校，同时得到了家长的一致好评和社会的认可。 洪伟教育价值观：用良心做事，用科学办事。 洪伟教育教学理念：用心教学，用爱育人，挖掘学生潜能，张扬学生个性。 洪伟教育校训： 求实创新 为学为教 洪伟教育教学目标：以培养和训练学生优秀思考、解题能力和方法为目标；以协同家庭共同教育，通过非智力因素开发智力和培养学习能力为目标。 洪伟教育培养目标：使学生喜欢学习，学会自我学习。 洪伟教育“N+1”教学团队：教育咨询师+心理专家+学习管理师+一个精英教学团队+一名专职班主任。 北京洪伟教育中心已经在激烈的竞争中挣得一席之地，即将揭开新的发展篇章，快速成长。在此我们诚挚向有志之士发出邀请，--------加入洪伟，成就未来！ www.bjhwjy.cn 全选 初中、高中各科骨干教师、学科带头人 北京市海淀外国语实验学校 地点：北京 语文教师 北京华乐思教育科技有限公司 地点：北京 AP经济教师 北京王府学校 地点：北京 数学教师 北京王府学校 地点：北京 高中地理老师 文甲(北京)教育文化有限公司 地点：北京 高中化学老师 文甲(北京)教育文化有限公司 地点：北京 高中历史老师 文甲(北京)教育文化有限公司 地点：北京 高中生物老师 文甲(北京)教育文化有限公司 地点：北京 高中英语老师 文甲(北京)教育文化有限公司 地点：北京 高中物理老师 文甲(北京)教育文化有限公司 地点：北京 全选 查看更多最新职位推荐 >> 全选 全选 查看更多相似职位推荐 >>",
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
    "description": "公司简介北京汇能精电科技股份有限公司（股票代码：830996）成立于2007年3月，是国内新能源行业的知名企业，是一家专业从事新能源电源产品研发、制造、销售为一体的北京市高新技术企业。公司坐落昌平区，拥有3000平方的研发大楼；公司于2014年7月在深圳市宝安区创建13000平方的生产制造基地。公司主要从事国际、国内先进水平智能网络化混合电源方案产品，如：太阳能电源控制器、太阳能电源控制逆变一体机、通信及电力专用逆变电源、专用混合电源网络配套智能仪表等产品的研制、开发、生产及销售， 以及各种电源应用系统的设计及工程服务。公司取得了iso9001―2008质量体系认证，cgc金太阳认证、ce认证等多项国内、国际权威认证；产品销往100多个国家，并且通过了国家质量检验中心的检测，获得了多项产品专利、软件著作权等。公司以“专业、创新、求实”为企业宗旨，以“诚信立足，创新致远”为理念，为用户提供精湛的技术、专业的产品、完善的服务；汇聚才能、打造精准电源，汇能精电―让您领先一步。让绿色能源造福全人类。公司员工300余人，其中高级研发、技术人员50余人。拥有强大的研发团队，安静优雅的办公环境和公平公正的晋升平台。产品在国内广泛使用，远销国外100多个国家和地区，在国内、外众多重大项目中应用并得到好评。公司产品以其优良的品质、完善的服务享誉国内外市场。联系电话：82894896-6108  15311995709公司主页：http://www.epever.com.cn",
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



