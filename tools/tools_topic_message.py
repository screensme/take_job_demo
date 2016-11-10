#!/usr/bin/env python
# encoding: utf-8

import sys
import random
import datetime
import time

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

    # 在消息中根据status，添加文字
    @classmethod
    def edit_message_status_info(cls, status=None, dt_time=datetime.datetime.now(), **kwargs):
        """1-->已预约,待同意，2-->已确认,待付款，3-->已付款,待约见，
        4-->已见面,待评价，10-->已评价,完成，11-->已取消，12-->未同意，13-->已过期，14-->未见面
        """
        if status == 1:
            dt_update_time = dt_time + datetime.timedelta(days=1)
            time_info = dt_update_time.strftime("%m/%d %H:%M")
            status_little_info = "行家将在 %s前给你回复" % time_info
            status_info = "约见已提交"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 2:
            dt_update_time = dt_time + datetime.timedelta(hours=6)
            time_info = dt_update_time.strftime("%m/%d %H:%M")
            status_little_info = "请在 %s前支付费用" % time_info
            status_info = "行家已同意"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 3:
            status_little_info = "已给出联系方式，请与行家确认好约见时间和地点"
            status_info = "约会费用已支付"
            kwargs = kwargs
        elif status == 4:
            status_little_info = "约会已见面，请你对本次见面做出评价"
            status_info = "已经见面"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 10:
            status_little_info = "本次约见已完成，希望对你有所帮助"
            status_info = "已完成"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 11:
            status_little_info = "你已取消本次预约"
            status_info = "预约已取消"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 12:
            status_little_info = "很遗憾，你的预约未通过，再去看看吧~"
            status_info = "行家未同意"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 13:
            status_little_info = "未在6小时内支付，预约已取消"
            status_info = "支付已过期"
            kwargs = {'mobile': '', 'email': ''}
        elif status == 14:
            status_little_info = "见面被取消，如需继续，请重新预约"
            status_info = "见面已取消"
            kwargs = {'mobile': '', 'email': ''}
        metadata = {'status_info': status_info,
                    'status_little_info': status_little_info,
                    'touch_info': kwargs}
        return metadata
