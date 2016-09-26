#!/usr/bin/env python
# encoding: utf-8
from tornado import gen
import time
import datetime
import json
import tornado.gen
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase
import requests
@tornado.gen.coroutine
# class MyTestCase3(AsyncTestCase):
def http_fetch():
    http_client = AsyncHTTPClient()
    url = "http://%s/%s" % ("127.0.0.1:8889", "idel_database" )
    # url = "http://%s/%s" % ("apimobile.zhaopintt.com:8889", "idel_database" )
    while True:
        try:
            response = yield http_client.fetch(url, method='post',
                                               body='key=%s' % "心跳线2016-9-9")
            req = json.loads(response.body)
            print (req)
            print ('---------------------We idel mysql. Success, time=%s' % datetime.datetime.now())
            time.sleep(3)
        except Exception, e:
            print ('---------------------We idel mysql. Fail, time=%s' % datetime.datetime.now())

def idel_post():
    url1 = "http://%s/%s" % ("127.0.0.1:8889", "idel_database" )
    url2 = "http://%s/%s" % ("127.0.0.1:8889", "idel_database" )
    url3 = "http://%s/%s" % ("127.0.0.1:8889", "idel_database" )
    # url1 = "http://%s/%s" % ("182.92.99.38:9002", "idel_database" )
    # url2 = "http://%s/%s" % ("182.92.99.38:9001", "idel_database" )
    # url3 = "http://%s/%s" % ("182.92.99.38:9000", "idel_database" )
    url_tuple = [url1, url2, url3]
    datas = {'key': "心跳线2016-9-9"}
    while True:
        try:
            for u in url_tuple:
                response = requests.post(url=u, data=datas)
                contect = response.content.decode('utf-8')
                print u + contect
                time.sleep(3)
        except Exception, e:
            print 'Hearbeat error = %s' % e
            continue

if __name__ == "__main__":
    # tornado.ioloop.IOLoop.current().run_sync(http_fetch())
    idel_post()
