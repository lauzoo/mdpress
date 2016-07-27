#!/usr/bin/env python
# encoding: utf-8
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_jwt import JWT
from redis import Redis
from jinja2 import BaseLoader, TemplateNotFound

login_manager = LoginManager()
admin = Admin()
jwt = JWT()
mail = Mail()


class RedisLoader(BaseLoader):
    def __init__(self):
        self.redis = Redis('127.0.0.1', 6379)

    def get_source(self, environment, template):
        prefix = self.redis.get('jinja:loader')
        path = "{}:{}".format(prefix, template)
        temp = self.redis.get(path)
        if not temp:
            raise TemplateNotFound(path)
        return temp, path, lambda: False
