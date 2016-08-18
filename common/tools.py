#!/usr/bin/env python
# encoding: utf-8

import json
# from bson.objectid import ObjectId
import datetime

#缺少参数
def args404(data):
    result = {}
    result['msg'] = 404
    result['status'] = 'fail'
    result['data'] = data
    return result


class ObjectToString(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, ObjectId):
        #     return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(ObjectToString, self).default(obj)
