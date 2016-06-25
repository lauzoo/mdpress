#!/usr/bin/env python
# encoding: utf-8
from flask_jwt import JWT
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.login import LoginManager


login_manager = LoginManager()
admin = Admin()
jwt = JWT()
mail = Mail()
