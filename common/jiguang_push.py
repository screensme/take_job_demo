#!/usr/bin/env python
# encoding: utf-8

#! /usr/bin/env python2
# encoding=utf-8
import time, random, json, sys, os
import requests
sys.path.insert(0,os.path.dirname(sys.path[0]))
reload(sys)
sys.setdefaultencoding('utf8')

#苹果的测试环境0,生产环境 v2
apns_production = 1
#苹果的测试环境0,生产环境 v3
apns_production_boolean = True

'''''
    极光key配置
'''
apps={
    'test':{
        "app_key" : u'app_key',
        "master_secret" : u'master_secret'
    },
    'product':{
        "app_key" : u'bcbcd55d31562e0cfef9050a',
        "master_secret" : u'2fa2a2b35a1f58224761220f'
    }
}

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
def jpush_v3(app_key, device_token, title, message, out_jump=None, in_jump=None):
    payload = {
            "platform": ["android", "ios"],     # "platform" : "all"
            "audience": {
                "registration_id" : device_token      # 推送给多个注册ID,['jfdksajfd54314','3j21jk321','3j2k1j32']
            },
            "notification": {       # 通知内容体
                "android": {
                    "alert": title,
                    "title": u"招聘头条",
                    "builder_id": 1,
                "extras": {
                    "key": out_jump
                }
                },
                "ios": {
                    "alert": title,
                    "sound": "default",
                    "badge": "+1",
                "extras": {
                    "key": out_jump
                }
                }
            },
            "message": {        # 消息内容体
                "msg_content": message,
                "content_type": "text",
                "title": "msg",
                "extras": {
                    "key": in_jump
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
    device_token = ['1a0018970aaeed0db6f']
    # device_token = ['1a0018970aaeed0db6f','160a3797c80cc710456']
    out_jump = ''
    in_jump = ''
    title = '我是一个段子手'
    message = '徐小污在此，还不快快受死！'
    jpush_v3(app_key=apps['product'], device_token=device_token,
             title=title, message=message, out_jump=out_jump, in_jump=in_jump)

# 各字段含义#####################################################
def push_message_to(app_key, app_secret, title, message, device_token):

    url = 'https://api.jpush.cn/v3/push'
    headers = "Content-Type: application/json"
    params = {
        "platform": ["android", "ios"],     # "platform" : "all"
        "audience": {
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