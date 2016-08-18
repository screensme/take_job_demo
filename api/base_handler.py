#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import tornado
import json
from tornado.web import HTTPError
from tornado import httputil

from common.tools import args404, ObjectToString


import logging
logger = logging.getLogger('boilerplate.' + __name__)

class BaseHandler(tornado.web.RequestHandler):

    def send_error(self, status_code=500, **kwargs):
        """
        Generates the custom HTTP error.And always return 200 code.

        """
        reason = None
        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
            if isinstance(exception, HTTPError) and exception.reason:
                reason = exception.reason
        try:
            msg = reason if reason else httputil.responses[status_code]
        except KeyError:
            msg = "unkown error"

        result = {"status_code":status_code, "reason": msg}

        self.clear()
        self.set_header("Content-Type", "application/json")
        self.set_status(200)
        self.write(ObjectToString().encode(result))
        self.finish()

    @property
    def db(self):
        return self.application.db

    @property
    def log(self):
        return self.application.log

    def check_args(self):
        d = None

        try:
            d = tornado.escape.json_decode(self.request.body)
        except ValueError, e:
            _ = 'decode track data error. e=%s' % e
            self._gen_response(status_txt='decode json error', log_message=_)
            return

        return d

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
            return self.request.arguments

        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg



    ### private help funcs
    def _gen_response(self, status_code=500, status_txt=None,log_message=None):
        r = {}
        self.log.error(log_message)
        r['status_code'] = status_code
        r['status_txt']  = status_txt

        self.write(ObjectToString().encode(r))
        self.finish()

    def get_cache_flag(self):
        try:
            cache_flag = self.get_argument('flag')
            c = int(cache_flag)
        except:
            c = 1
        return c

    def get_arguments(self):
        error = {}
        for key in self.request.arguments:
            error[key] = self.get_argument(key)
        return error
