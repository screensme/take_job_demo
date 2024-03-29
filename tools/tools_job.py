#!/usr/bin/env python
# encoding: utf-8

import sys
import random

reload(sys)
sys.setdefaultencoding("utf-8")


class EditNone(object):

    # 修改None --> ''
    @classmethod
    def edit_none(cls, *args):
        for index in args:
            if args[index] == None:
                args[index] = ''
        return args

    # 修改full-全职
    @classmethod
    def edit_type(cls, *args):
        for index in args:
            if index['job_type'] == 'fulltime':
                index['job_type'] = '全职'
            elif index['job_type'] == 'parttime':
                index['job_type'] = '兼职'
            elif index['job_type'] == 'intern':
                index['job_type'] = '实习'
            elif index['job_type'] == 'unclear':
                index['job_type'] = '不限'
        return args

    # 修改金额为K，logo，full-全职
    @classmethod
    def edit_k_logo_type(cls, image, *args):
        for index in args:
            index['salary_start'] = index['salary_start'] / 1000
            if (index['salary_end'] % 1000) >= 1:
                index['salary_end'] = index['salary_end'] / 1000 + 1
            else:
                index['salary_end'] = index['salary_end'] / 1000
            if index['company_logo'] != '':
                index['company_logo'] = "%s" % image + index['company_logo']
            else:
                index['company_logo'] = "%s" % image + "icompany_logo_%d.png" % (random.randint(1, 16),)
            index['id'] = index['jobid']
            if index['job_type'] == 'fulltime':
                index['job_type'] = '全职'
            elif index['job_type'] == 'parttime':
                index['job_type'] = '兼职'
            elif index['job_type'] == 'intern':
                index['job_type'] = '实习'
            elif index['job_type'] == 'unclear':
                index['job_type'] = '不限'
        return args

    # 修改图片 image 前缀加上self.image
    @classmethod
    def edit_image(cls, self_image, *args):
        for index in args:
            image = index.get('image', '')
            if image != '':
                index['image'] = "%s" % self_image + image
        return args

    # 修改图片 little_image 前缀加上self.image
    @classmethod
    def edit_little_image(cls, self_image, *args):
        for index in args:
            image = index.get('little_image', '')
            if image != '':
                index['little_image'] = "%s" % self_image + image
        return args

    # 修改图片 avatar 前缀加上self.image
    @classmethod
    def edit_avatar(cls, self_image, *args):
        for index in args:
            avatar = index.get('avatar', '')
            if avatar != '' and (avatar is not None):
                index['avatar'] = "%s" % self_image + avatar
        return args

    # 修改图片 little_image,avatar 前缀加上self.image
    @classmethod
    def edit_avatar_littleimage(cls, self_image, *args):
        for index in args:
            avatar = index.get('avatar', '')
            little_image = index.get('little_image', '')
            if avatar != '' and (little_image != ''):
                index['avatar'] = "%s" % self_image + avatar
                index['little_image'] = "%s" % self_image + little_image
        return args

