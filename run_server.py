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
from common.web_config import MY_SQL, ES_API
from database import Action
define("port", default=8889, help="run on the given port", type=int)
define("mysql", default='neiwang', help="run on the test or pro")
define("esapi", default='neiwang', help="run on the test or pro")

# def main():
#     tornado.options.parse_command_line()
#     app = Application()
#     app.listen(options.port, '0.0.0.0')
#
#     try:
#         tornado.ioloop.IOLoop.instance().start()
#         print("\nstart server.")
#     except KeyboardInterrupt:
#         print("\nStopping server.")
#
# class Application(tornado.web.Application):
#     def __init__(self):
#         debug = 1
#         tornado.web.Application.__init__(self, urls, **settings)
#         self.db = Action.Action(dbhost='123.57.33.133', dbport=27017, dbname='worry1613', dbuser='xSD6!nw1U*SqNfC4', dbpwd='huoban')
# if __name__ == "__main__":
#     main()


abp = os.path.abspath(sys.argv[0])
file_path = os.path.dirname(abp) + '/json_txt'

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "XjC20zUNROW+EKe/wpeYCyRD1AuntU8cqdyBNQSPfT8=",
    "login_url": "/login/",
    "xsrf_cookies": False,
    "debug": True,
    "siteDomain": "/HUUO/",
    "siteURL": "",
    "staticURL": "",
    "siteName": "",
    'file_path': file_path,
    # "ui_modules": ui_modules,
    # "db": db,
    # 'server': my_server,
    # "cache": cache,
    # "scriptlist": scriptlist,
    # "scriptsha":  scriptsha,
    # "gulipaTime": datetime.datetime(2015, 2, 14),
    # "log": log
}

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict()
        tornado.web.Application.__init__(self, urls, **settings)
        self.log = web_log.debugf("")
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates'),
        mysqlstr = 'mysql-%s' % options.mysql
        esapistr = 'esapi-%s' % options.esapi
        self.db = Action.Action(dbhost=MY_SQL[mysqlstr]['host'],
                                # dbport=MY_SQL[mysqlstr]['port'],
                                dbname=MY_SQL[mysqlstr]['db'],
                                dbuser=MY_SQL[mysqlstr]['user'],
                                dbpwd=MY_SQL[mysqlstr]['pwd'],
                                log=self.log,
                                esapi=ES_API[esapistr]['url']
                                )


def creator_server():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port, '0.0.0.0')
    app.log.debug("load finished! listening on %s:%s" % ('127.0.0.1', options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    creator_server()
