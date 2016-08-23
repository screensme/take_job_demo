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
    'mysql-waiwang': {'host': '182.92.99.38:3306',
                      # 'port': '',
                      'db': 'rcat_test',
                      'user': 'probie_test',
                      'pwd': 'tt_probie'
                      }}
ES_API = {
    'esapi-neiwang': {
        'url': 'http://192.168.12.146:8000/'
    },
    'esapi-waiwang': {
        'url': 'http://182.92.99.38:8000/'
    }
}
FCGI_SETTIGNS = {
    'fcgi_port': 1024,
}