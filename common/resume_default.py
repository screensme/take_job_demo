#!/usr/bin/env python
# encoding: utf-8

cv_dict_default = {
    'basic': {
        'education': '',
        'name': '',
        'current_area': '',
        'phonenum': '',
        'email': '',
        'marital_status': '',
        'avatar': '',
        'birthday': '',
        'politics_status': '',
        'gender': ''
    },
    # 求职意向
    'intension': {
        'status': '',
        'trade': '',
        'area': '',
        'title': '',
        'expect_salary': '',
    },
    # 教育经历
    'education': [
        {
            'school': '',
            'major': '',
            'start_time': '',
            'end_time': '',
            'classroom': '',
            'degree': '',
        },
    ],
    # 工作/实习经历
    'career': [
        {
            'company': '',
            'trade': '',
            'title': '',
            'area': '',
            'start_time': '',
            'end_time': '',
            'duty': '',
        },
    ],

    # 项目经验/社会实践
    'experience': [
        {
            'title': '',
            'project_name': '',
            'start_time': '',
            'end_time': '',
            'description': '',
        },
    ],
    # 校内职务
    'school_job': [
        {
            'job_name': '',
            'school_name': '',
            'start_time': '',
            'end_time': '',
            'job_info': '',
        }
    ],

    # 校内奖励
    'school_rewards': [
        {
            'rewards_name': '',
            'school_name': '',
            'start_time': '',
            'end_time': '',
            'rewards_info': '',
        }
    ],

    # 语言能力
    'languages': [
        {
            'language_name': '',
            'hear': '',
            'readwrite': '',
        }
    ],
    # IT技能
    'skill': [
        {
            'skill_name': '',
            'skill_level': '',
            'skill_time': '',
        }
    ],
    # 获得证书
    'certificate': [
        {
            'certificate_name': '',
            'certificate_level': '',
            'certificate_time': '',
        }
    ],
    # 其他信息
    'extra': {
        'title': '',
        'description': '',
    },

}