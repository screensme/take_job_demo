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
    'esapi-neiwang': {
        'url': 'http://192.168.12.146:8000/'
    },
    'esapi-waitest': {
        'url': 'http://182.92.202.243:8000/'
    },
    'esapi-waiwang': {
        'url': 'http://182.92.99.38:8000/'
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
        'host': '192.168.12.146',
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
        'host': '182.92.99.38',
        'port': 6379,
        'password': '',
        'db': 1
    },
    'redis-online': {
        'host': '23fef09bdd5a4810.m.cnbja.kvstore.aliyuncs',
        'port': 6379,
        'password': 'Rcat123ABCD',
        'db': 1
    }
}
REDIS_URL = 'redis://23fef09bdd5a4810:Rcat123ABCD@23fef09bdd5a4810.m.cnbja.kvstore.aliyuncs.com/1'
# user / password @ ip:port / db
# 23fef09bdd5a4810.m.cnbja.kvstore.aliyuncs.com ---> 100.114.45.27
FCGI_SETTIGNS = {
    'fcgi_port': 1024,
}