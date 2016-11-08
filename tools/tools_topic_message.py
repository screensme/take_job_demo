#!/usr/bin/env python
# encoding: utf-8

import sys
import random

reload(sys)
sys.setdefaultencoding("utf-8")


class EditTopic(object):

    # 修改None --> ''
    @classmethod
    def edit_none(cls, *args):
        for index in args:
            if args[index] == None:
                args[index] = ''
        return args

    # 修改话题状态status，为汉字
    @classmethod
    def edit_status_process(cls, *args):
        for index in args:
            if index['status'] == 1:
                index['status'] = '待同意'
            if index['status'] == 2:
                index['status'] = '待付款'
            if index['status'] == 3:
                index['status'] = '待约见'
        return args
