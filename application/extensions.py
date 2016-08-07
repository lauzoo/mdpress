#!/usr/bin/env python
# encoding: utf-8
import os
import time

from flask import current_app

from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_jwt import JWT
from flask_redis import FlaskRedis
from flask.ext.elasticsearch import FlaskElasticsearch
from redis import Redis
from jinja2 import BaseLoader, TemplateNotFound


jwt = JWT()
mail = Mail()
admin = Admin()
redis = FlaskRedis()
login_manager = LoginManager()
es = FlaskElasticsearch()


class RedisLoader(BaseLoader):
    def __init__(self):
        self.redis = Redis('127.0.0.1', 6379)

    def get_source(self, environment, template):
        current_app.logger.debug("load template: {}".format(template))
        template_prefix = 'mdpress:template:theme'
        if template[:6] == "admin/":
            key = "{}:{}".format(template_prefix, template)
        else:
            theme = self.redis.get('mdpress:theme')
            key = "{}:{}/{}".format(template_prefix, theme, template)
        lm_key = "{}:lm".format(key)
        path_key = "{}:path".format(key)

        path = self.redis.get(path_key)
        last_modified = redis.get(lm_key)

        if not path or not last_modified:
            current_app.logger.debug("template path: {}".format(path))
            current_app.logger.debug("template last modified: {}".format(last_modified))
            raise TemplateNotFound(key)
        curr_last_modified = time.ctime(os.path.getmtime(path))
        if last_modified != curr_last_modified:
            with open(path, 'r') as f:
                data = f.read()
                self.redis.set(key, data)
                self.redis.set(lm_key, curr_last_modified)
        temp = self.redis.get(key)
        return temp, key, lambda: False
