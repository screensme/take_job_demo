#!/usr/bin/env python
# encoding: utf-8

import requests
from multiprocessing.pool import ThreadPool
import json
import os, sys
"""         调用es的各种接口           """

abp = os.path.abspath(sys.argv[0])
file_path = os.path.dirname(abp)


class QueryEsapi(object):

    def __init__(self, esapi, log):
        self.esapi = esapi
        self.log = log

    @classmethod
    def query_trade_top(cls, esapi, trade='不限', work_years='不限'):
        url = esapi + 'query_trade_top'
        ret_value = None

        if work_years == '不限':
            work_years = (-1, 1)
        work_years_start, work_years_end = work_years
        if work_years_start < 0:
            work_years_start = 0
        if trade == '不限':
            trade = None

        ret = {
            'work_years_start': work_years_start,
            'work_years_end': work_years_end,
            'trade': trade,
        }

        payload = {k: v for k, v in ret.items() if v is not None}
        try:
            r = requests.post(url, json=payload)
            ret_value = r.json()
        except Exception as e:
            # self.log.info('11111')
            ret_value = []

        ret_value = [{'job_name': item[0], 'salary_avg':
                      int(item[1])} for item in ret_value]

        for i in range(0,len(ret_value)):
            if ret_value[i]['job_name'] in ['健身顾问','信用卡专员']:
                ret_value[i]['salary_avg'] -= 3000
                continue
            if i > 8:
                ret_value[i]['salary_avg'] = int(1.1 * ret_value[i]['salary_avg'])

        ret_value = sorted(ret_value, key=lambda x:x['salary_avg'], reverse=True)
        ret_value = [{'job_name': item['job_name'],
                      'salary_avg': format(int(item['salary_avg']))} for item in ret_value]
        return ret_value

    # 查询多个职位平均工资
    @classmethod
    def query_multi_job_top(cls, esapi, *hot_job_list):
        job_list = list(set(hot_job_list))
        job_top_list = []

        if len(job_list) == 0:
            return job_top_list

        pool_num = len(job_list)
        pool = ThreadPool(pool_num)
        tmp_list = []

        # 同时请求
        for job in job_list:
            payload = {
                'esapi': esapi,
                'job_name': job.strip(),
                'work_years': '应届',
            }
            tmp_value = pool.apply_async(QueryEsapi.query_job_salary_avg, kwds=payload)
            tmp_list.append(tmp_value)

        pool.close()
        # 结果
        job_top_list = [item.get() for item in tmp_list if item.get() is not None]
        job_top_list.sort(key=lambda x:x['salary_avg'], reverse=True)

        return job_top_list

    @classmethod
    def query_job_salary_avg(cls, esapi, job_name='不限', work_years='不限'):
        url = esapi + 'query_job_salary_avg'
        if work_years:
            work_years = (-1, 1)

        if job_name == '不限':
            job_name = None

        # 判断job_name是否是在职位白名单里面
        with open(file_path+'/helpers/major_job_list.json') as f:
            major_job_list = json.load(f)

        major_job_list = [item.strip().upper() for item in major_job_list]
        if job_name.strip().upper() in major_job_list:

            work_years_start, work_years_end = work_years
        else:
            work_years_start, work_years_end = None, None
        if work_years_start < 0:
            work_years_start = 0
        ret = {
            'work_years_start': work_years_start,
            'work_years_end': work_years_end,
            'job_name': job_name
        }

        payload = {k: v for k, v in ret.items() if v is not None}

        try:
            r = requests.post(url, json=payload)
            ret_value = r.json()
            if ret_value['salary_avg'] is None:
                ret_value = None
            else:
                ret_value['salary_avg'] = int(ret_value['salary_avg'])
        except Exception as e:
            ret_value = None

        return ret_value

#   ##############################计算平均薪资
    @classmethod
    # 调用平均薪资
    def use_query_map(cls, **payload):

        pool = ThreadPool(9)
        th_salary_tantile_list = pool.apply_async(QueryEsapi.query_job_salary_avg_all, kwds=payload)
        return th_salary_tantile_list

    # 平均薪资
    @classmethod
    def query_job_salary_avg_all(cls, esapi, job_name='不限', work_years='不限'):
        url = esapi + 'query_job_salary_avg'
        if work_years:
            work_years = (-1, 1)

        if job_name == '不限':
            job_name = None

        # 判断job_name是否是在职位白名单里面
        with open(file_path+'/helpers/major_job_list.json') as f:
            major_job_list = json.load(f)

        major_job_list = [item.strip().upper() for item in major_job_list]
        if job_name.strip().upper() in major_job_list:
            work_years_start, work_years_end = work_years
        else:
            work_years_start, work_years_end = None, None

        ret = {
            'work_years_start': work_years_start,
            'work_years_end': work_years_end,
            'job_name': job_name
        }

        payload = {k: v for k, v in ret.items() if v is not None}

        try:
            r = requests.post(url, json=payload)
            ret_value = r.json()
            if ret_value['salary_avg'] is None:
                ret_value = None
            else:
                ret_value['salary_avg'] = int(ret_value['salary_avg'])
        except Exception as e:
            # self.logger.exception(e)
            ret_value = None

        return ret_value


#   ##############################计算平均工作年限
    @classmethod
    # 调用工作年限
    def use_query_avg_work_years(cls, **payload):

        pool = ThreadPool(9)
        th_salary_tantile_list = pool.apply_async(QueryEsapi.query_avg_work_years, kwds=payload)
        return th_salary_tantile_list

    # 平均工作年限
    @classmethod
    def query_avg_work_years(cls, esapi, job_name='', job_city='北京', area=''):
        url = esapi + 'query_avg_work_years'

        payload = {
            'job_name': job_name,
            'job_city': job_city,
            'area': area,
        }

        try:
            r = requests.post(url, json=payload)
            ret_value = r.json()
            ret_value = round(ret_value, 1)
        except Exception as e:
            # self.logger.exception(e)
            ret_value = 3

        return ret_value

#   ##########################################################################################

    @classmethod
    # 调用饼图接口
    def use_query_map(cls, **payload):

        pool = ThreadPool(9)
        th_salary_tantile_list = pool.apply_async(QueryEsapi.query_map, tuple(), payload)
        return th_salary_tantile_list

    @classmethod
    # 饼图(工资区间分布，工作年限分布， 教育背景)
    def query_map(cls, esapi, job_name='', search_type=None, job_city='北京', area=''):
        url = esapi + 'query_percent'
        search_type_tuple = ('salary', 'work_years', 'education')

        ret_value = []

        if search_type not in search_type_tuple:
            return ret_value

        payload = {
            'job_name': job_name,
            'search_type': search_type,
            'job_city': job_city,
            'area': area,
        }

        try:
            r = requests.post(url, json=payload)
            ret_value = r.json()
            if '面议' in ret_value:
                ret_value.pop('面议')
            total = sum(ret_value.values())
        except Exception as e:
            # self.logger.exception(e)
            ret_value = {}

        ret_list = []

        search_type_dict = {
            'salary': [
                    '3k以下',
                    '3k-5k',
                    '5k-8k',
                    '8k-12k',
                    '12k-15k',
                    '15k-20k',
                    '20k-25k',
                    '25k-30k',
                    '30k-40k',
                    '40k-50k',
                    '50k以上'
            ],
            'work_years': [
                        '应届毕业生',
                        '1-3年',
                        '3-5年',
                        '5-10年',
                        '10年以上',
            ],
            'education': [
                    '中专',
                    '大专',
                    '本科',
                    '硕士',
                    '博士',
            ],
        }

        if len(ret_value) > 0:
            for key in search_type_dict[search_type]:
                value = ret_value.get(key.decode('utf-8'), 0)
                if value != 0:
                    value = float(value) / float(total)
                    value = round(value * 100, 2)

                ret_list.append((key,value))

        return ret_list

if __name__ == "__main__":
    s = QueryEsapi()
    b = s.query_trade_top()
