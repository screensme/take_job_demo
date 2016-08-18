#!/usr/bin/env python
# encoding: utf-8

import tornado
import tornado.web, tornado.ioloop
import tornado.httpserver
from settings import settings
from tornado.options import options, define
import os, sys
from url_tt.url import urls
from database import Action
define("port", default=8888, help="run on the given port", type=int)

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
        handlers = urls,
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates'),
        settings = dict()
        # self.db = Action.Action(dbhost='123.57.33.133',dbport=3306,dbname='huoban',dbuser='worry1613',dbpwd='xSD6!nw1U*SqNfC4')
        tornado.web.Application.__init__(self, handlers, **settings)

def creator_server():

    app = tornado.web.Application(
        handlers=urls,
        **settings
        )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    creator_server()
    print('init')