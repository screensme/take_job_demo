#!/usr/bin/env python
# encoding: utf-8
import tornado
import tornado.web, tornado.ioloop
import tornado.httpserver
from settings import settings
from tornado.options import options, define
import os, sys
from url_tt.url import urls
from common import web_log
from configs.web_config import MY_SQL, ES_API, REDIS, IMAGE_URL
from database import Action
from common import query_top
define("port", default=8889, help="run on the given port", type=int)
define("mysql", default='neiwang', help="run on the test or pro")
define("esapi", default='neiwang', help="run on the test or pro")
define("redis", default='local', help="run on the test or pro")
define("sms", default='no', help="true=yes,false=no(send:111111)")
define("image", default='neiwang', help="run on the test or pro")
#
# abp = os.path.abspath(sys.argv[0])
# file_path = os.path.dirname(abp) + '/json_txt'
#
# settings = {
#     "static_path": os.path.join(os.path.dirname(__file__), "static"),
#     "cookie_secret": "XjC20zUNROW+EKe/wpeYCyRD1AuntU8cqdyBNQSPfT8=",
#     "login_url": "/login/",
#     "xsrf_cookies": False,
#     "debug": True,
#     "siteDomain": "/HUUO/",
#     "siteURL": "",
#     "staticURL": "",
#     "siteName": "",
#     'file_path': file_path,
#     # "ui_modules": ui_modules,
#     # "db": db,
#     # 'server': my_server,
#     # "cache": cache,
#     # "scriptlist": scriptlist,
#     # "scriptsha":  scriptsha,
#     # "gulipaTime": datetime.datetime(2015, 2, 14),
#     # "log": log
# }

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict()
        tornado.web.Application.__init__(self, urls, **settings)
        web_log.init()
        self.log = web_log.debugf("")
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates'),
        sms = options.sms
        mysqlstr = 'mysql-%s' % options.mysql
        esapistr = 'esapi-%s' % options.esapi
        redisstr = 'redis-%s' % options.redis
        imagestr = 'image-%s' % options.image
        self.db = Action.Action(dbhost=MY_SQL[mysqlstr]['host'],
                                dbname=MY_SQL[mysqlstr]['db'],
                                dbuser=MY_SQL[mysqlstr]['user'],
                                dbpwd=MY_SQL[mysqlstr]['pwd'],
                                log=self.log,
                                sms=sms,
                                image=IMAGE_URL[imagestr]['url'],
                                esapi=ES_API[esapistr]['url'],
                                cahost=REDIS[redisstr]['host'],
                                caport=REDIS[redisstr]['port'],
                                capassword=REDIS[redisstr]['password'],
                                caseldb=REDIS[redisstr]['db']
                                )
        self.query = query_top.QueryEsapi(esapi=ES_API[esapistr]['url'],
                                          log=self.log
                                          )


def creator_server():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port, '0.0.0.0')
    app.log.debug("load finished! listening on %s:%s" % ('127.0.0.1', options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    creator_server()
