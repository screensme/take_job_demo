#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import inspect,os

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
LOG_PATH = SITE_ROOT + "/log/"

MY_SQL = {
    'mysql-neiwang': {'host': '192.168.12.146:3306',
                      # 'port': 3306,
                      'db': 'rcat_test',
                      'user': 'probie_test',
                      'pwd': 'tt_probie'
                      },
    'mysql-waitest': {'host': '182.92.202.243:3306',
                      # 'port': '',
                      'db': 'rcat_test',
                      'user': 'probie_test',
                      'pwd': 'tt_probie'
                      },
    'mysql-waiwang': {'host': '182.92.99.38:3306',
                      # 'port': '',
                      'db': 'rcat_test',
                      'user': 'probie_test',
                      'pwd': 'tt_probie'
                      },
    'mysql-online': {'host': 'rds6zqwqw8amt8v02464.mysql.rds.aliyuncs.com:3306',
                      # 'port': '',
                      'db': 'cainiao',
                      'user': 'user_01',
                      'pwd': 'yigehenchanghenchangdemima'
                      }
}
ES_API = {
    'esapi-worry': {
        'url': 'http://192.168.12.178:8000/'
    },
    'esapi-neiwang': {
        'url': 'http://192.168.12.146:8000/'
    },
    'esapi-waitest': {
        'url': 'http://182.92.202.243:8000/'
    },
    'esapi-waiwang': {
        'url': 'http://100.98.226.26:6000/'
    },
    'esapi-online': {
        'url': 'http://100.98.226.26:6000/'
    }
}

IMAGE_URL = {
    'image-neiwang': {
        'url': 'http://imgtest.zhaopintt.com/'
    },
    'image-waitest': {
        'url': 'http://imgtest.zhaopintt.com/'
    },
    'image-waiwang': {
        'url': 'http://images.zhaopintt.com/'
    }
}

REDIS = {
    'redis-local': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 1
    },
    'redis-neiwang': {
        'host': '192.168.12.157',
        'port': 6379,
        'password': '',
        'db': 1
    },
    'redis-waitest': {
        'host': '182.92.202.243',
        'port': 6379,
        'password': '',
        'db': 1
    },
    'redis-waiwang': {
        'host': '23fef09bdd5a4810.m.cnbja.kvstore.aliyuncs.com',
        'port': 6379,
        'password': 'Rcat123ABCD',
        'db': 1
    },
    'redis-online': {
        'host': '23fef09bdd5a4810.m.cnbja.kvstore.aliyuncs.com',
        'port': 6379,
        'password': 'Rcat123ABCD',
        'db': 1
    }
}

BASE_URL = {
    'BASE_URL-neiwang': {
        'url': 'http://192.168.33.10:8000/',
        },
    'BASE_URL-waitest': {
        'url': 'http://182.92.202.243:5000/',
        },
    'BASE_URL-waiwang': {
        'url': 'http://182.92.99.38:8888/',
    }
}

FCGI_SETTIGNS = {
    'fcgi_port': 1024,
}

API_KEY = 'a6a724c40f5c908e9a44f93d46dad99e'

'''
    极光key配置
'''
JPUSH_SETTINGS = {
    'test':{
        "app_key" : 'app_key',
        "master_secret" : 'master_secret'
    },
    'product':{
        "app_key": 'bcbcd55d31562e0cfef9050a',
        "master_secret": '2fa2a2b35a1f58224761220f'
    }

    }

# ping++ id
Test_Secret_Key = "sk_test_jPK4GKWLOCW94av5i5nTmrjL"
Live_Secret_Key = "sk_live_X9ajj1TCa1u15Si94ObzLWDS"

pingpp_app_key = "app_eTiLm1mvTGe5O4mv"
pingpp_api_key = {'test_test': Test_Secret_Key,
                  'true_true': Live_Secret_Key}