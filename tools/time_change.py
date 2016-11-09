#!/usr/bin/env python
# encoding: utf-8

import sys
import datetime
# import random

reload(sys)
sys.setdefaultencoding("utf-8")


class Time_Change(object):

    # 转换为格式： 年-月-日 时：分：秒
    @classmethod
    def string_time(cls, time_need_change=datetime.datetime.now()):
        # 转换为指定的格式:
        otherStyleTime = time_need_change.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

