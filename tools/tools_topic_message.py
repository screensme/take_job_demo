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
            elif index['status'] == 2:
                index['status'] = '待付款'
            elif index['status'] == 3:
                index['status'] = '待约见'
            elif index['status'] == 4:
                index['status'] = '待评价'
            elif index['status'] == 10:
                index['status'] = '已结束'
            elif index['status'] == 11:
                index['status'] = '已取消'
            elif index['status'] == 12:
                index['status'] = '已过期'
            elif index['status'] == 13:
                index['status'] = '未同意'
        return args
