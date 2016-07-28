#!/usr/bin/env python
# encoding: utf-8
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_jwt import JWT
from flask_redis import FlaskRedis
from redis import Redis
from jinja2 import BaseLoader, TemplateNotFound

login_manager = LoginManager()
admin = Admin()
jwt = JWT()
redis = FlaskRedis()
mail = Mail()


class RedisLoader(BaseLoader):
    def __init__(self):
        self.redis = Redis('127.0.0.1', 6379)

    def get_source(self, environment, template):
        template_prefix = self.redis.get('mdpress:template:theme')
        path = "{}:{}".format(template_prefix, template)
        temp = self.redis.get(path)
        if not temp:
            raise TemplateNotFound(path)
        return temp, path, lambda: False
