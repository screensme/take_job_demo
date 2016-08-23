#!/usr/bin/env python
# encoding: utf-8
"""
logger 需求：
1. 自动定时清除日志，分日、小时两种级别
2. 模块可以启用自己的日志级别
3. 模块可以启用自己的日记域
"""

from __future__ import unicode_literals

import time
import logging

from logging.handlers import TimedRotatingFileHandler
from common.web_config import FCGI_SETTIGNS, LOG_PATH


#TODO move to it pub logic, not in app logic
class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        record is not used, as we are just comparing times, but it is needed so
        the method signatures are the same
        """
        #change for 'H'
        if self.when == 'H':
            t = time.localtime(self.rolloverAt)
            currentYear = t[0]
            currentMon = t[1]
            currentDay = t[2]
            currentHour = t[3]
            self.rolloverAt = int(time.mktime((currentYear,currentMon,currentDay,currentHour,0,0,0,0,0)))
        elif self.when == 'D':
            t = time.localtime(self.rolloverAt)
            currentYear = t[0]
            currentMon = t[1]
            currentDay = t[2]
            self.rolloverAt = int(time.mktime((currentYear,currentMon,currentDay,0,0,0,0,0,0)))

        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0


def init(loglevel=logging.DEBUG, errlevel=logging.ERROR, log_path=LOG_PATH, filemode='a'):
    """ init the logger, must be called at first
    """
    root_log = logging.getLogger('')
    root_log.setLevel(loglevel)

    rotateHandler = MyTimedRotatingFileHandler(log_path+str(FCGI_SETTIGNS['fcgi_port'])+'.log', 'D')
    rotateHandler.setLevel(loglevel)
    rotateHandler.setFormatter(logging.Formatter(
        '%(asctime)s $%(process)d--%(threadName)s %(name)s %(levelname)s %(filename)s: #%(lineno)d %(message)s'))
    root_log.addHandler(rotateHandler)

    errHandler = MyTimedRotatingFileHandler(log_path+str(FCGI_SETTIGNS['fcgi_port'])+'.err', 'D')
    errHandler.setLevel(errlevel)
    errHandler.setFormatter(logging.Formatter(
        '%(asctime)s $%(process)d--%(threadName)s %(name)s %(levelname)s %(filename)s: #%(lineno)d %(message)s'))
    root_log.addHandler(errHandler)

def debugf(modulename):
    """ debugf wrapper
    """
    return logging.getLogger(modulename)
