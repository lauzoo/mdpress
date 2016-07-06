#!/usr/bin/env python
# encoding: utf-8
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask_jwt import JWT

login_manager = LoginManager()
admin = Admin()
jwt = JWT()
