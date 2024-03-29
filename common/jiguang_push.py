#!/usr/bin/env python
# encoding: utf-8

import time, random, json, sys, os
import requests
from configs.web_config import JPUSH_SETTINGS

sys.path.insert(0,os.path.dirname(sys.path[0]))
reload(sys)
sys.setdefaultencoding('utf8')

#苹果的测试环境0,生产环境 v2
apns_production = 1
#苹果的测试环境0,生产环境 v3
apns_production_boolean = True



'''''
    https request jpush v3
'''
def https_request(app_key,body, url, content_type=None,version=None, params=None):
    https = requests.Session()
    https.auth = (app_key['app_key'], app_key['master_secret'])
    headers = {}
    headers['user-agent'] = 'jpush-api-python-client'
    headers['connection'] = 'keep-alive'
    headers['content-type'] = 'application/json;charset:utf-8'
    #print url,body
    response = https.request('POST', url, data=body, params=params, headers=headers)
    #合并返回
    print response.status_code, response.content
    return dict(json.loads(response.content) , **{'status_code':response.status_code})

'''''
    jpush v3 params
    支持离线消息，在线通知同时发送
'''
# def push_params_v3(content,receiver_value=None,n_extras=None,platform="ios,android"):
#     global apns_production_boolean
#     sendno = int(time.time()+random.randint(10000000,99999900))
#     payload =dict()
#     payload['platform'] =platform
#
#     payload['audience'] ={
#         "alias" : receiver_value
#     }
#     #离线消息
#     payload['message'] = {
#         "msg_content" : content,
#         "extras" : n_extras
#     }
#     #在线通知
#     payload['notification'] = {
#         "android" : {"alert" : content,"extras" : n_extras},
#         "ios"     : {"alert" : content,"sound":"default","extras" : n_extras},  #"badge":1,
#     }
#     payload['options'] ={"apns_production":apns_production_boolean,"time_to_live":86400*3,'sendno':sendno}
#
#     return payload

'''''
    jpush v3 request 简单版
'''
def jpush_v3(app_key, device_token, title, message, push_type=None, push_code=None):
    payload = {
            "platform": ["android", "ios"],     # "platform" : "all"
            "audience": {
                "registration_id" : device_token      # 推送给多个注册ID,['jfdksajfd54314','3j21jk321','3j2k1j32']
            },
            "notification": {       # 通知内容体(在窗口可见的推送)
                "android": {
                    "alert": title,
                    "title": u"招聘头条",
                    "builder_id": 1,
                "extras": {
                    "push_type": push_type,
                    "push_code": push_code
                }
                },
                "ios": {
                    "alert": title,
                    "sound": "default",
                    "badge": "+1",
                "extras": {
                    "push_type": push_type,
                    "push_code": push_code
                }
                }
            },
            "message": {        # 消息内容体（APP内可见的推送）相当于"离线推送"
                "msg_content": message,
                "content_type": "text",
                "title": "msg",
                "extras": {
                    "push_type": push_type,
                    "push_code": push_code
                }
            },
            "options": {
                "time_to_live": 86400*3,
                "apns_production": False    # True 表示推送生产环境，False 表示要推送开发环境
            }
        }
    body = json.dumps(payload)
    #print body
    return https_request(app_key,body, "https://api.jpush.cn/v3/push",'application/json', version=1)

if __name__ == "__main__":
    device_token = ['171976fa8a88db9e85b']
    # device_token = ['13165ffa4e00e1c1e8c','160a3797c80cc710456','171976fa8a88db9e85b']
    push_type = 20
    push_code = random.randint(21,24)
    title = '欲罢不能造句'+ str(push_code)
    # message = '老师：请用欲罢不能造个句，我一同学悠悠地来了句：“昨天我家浴霸不能用了，洗个澡冻死爹了。”'
    message = '有个人问我：你们北京人凭什么那么牛逼？我默默的深吸了一口气，笑着看了看他。他不服，硬要学我，也深吸了一口气……享年36岁！'
    jpush_v3(app_key=JPUSH_SETTINGS['product'], device_token=device_token,
             title=title, message=message, push_type=push_type, push_code=push_code)

# -=-=-=-=-=-=-=-=-=-
# 各字段含义#####################################################
def push_message_to(app_key, app_secret, title, message, device_token):

    url = 'https://api.jpush.cn/v3/push'
    headers = "Content-Type: application/json"
    params = {
        "platform": ["android", "ios"],     # "platform" : "all"
        "audience": {   # 里面至少选择一种推送方式
            # "tag": ["深圳", "广州" ],    # 推送给多个标签
            # "alias": ["4314", "892", "4531"],    # 推送给多个别名
            # "tag_and": ["女", "会员"],   # 推送给多个标签
            "registration_id" : device_token      # 推送给多个注册ID,['jfdksajfd54314','3j21jk321','3j2k1j32']
        },
        "notification": {       # 通知内容体
            "android": {
                "alert": title,
                "title": "Send to Android",
                "builder_id": 1,
                "extras": {     # 自定义字段
                    "newsid": 321
                }
            },
            "ios": {
                "alert": title,
                "sound": "default",
                "badge": "+1",
                "extras": {
                    "newsid": 321
                }
            }
        },
        "message": {        # 消息内容体
            "msg_content": message,
            "content_type": "text",
            "title": "msg",
            "extras": {
                "key": "value"
            }
        },
        # "sms_message":{
        #     "content":"sms msg content",
        #     "delay_time":3600
        # },
        "options": {
            "time_to_live": 60,
            "apns_production": False    # True 表示推送生产环境，False 表示要推送开发环境
        }
    }