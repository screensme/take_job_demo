__author__ = 'XV'

import tornado
import tornado.web
from common import web_log
from url_tt import url
from settings import settings
from common.web_config import MY_SQL, IMAGE_URL, ES_API, REDIS
from database import Action

mysqlstr = "mysql-neiwang"
sms = "no"
imagestr = "image-neiwang"
esapistr = "esapi-neiwang"
redisstr = "redis-neiwang"
class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url, **settings)
        web_log.init()
        self.log = web_log.debugf("")
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
        tornado.web.Application().listen(8888, '0.0.0.0')