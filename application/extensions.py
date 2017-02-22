#!/usr/bin/env python
# encoding: utf-8
import os
import time

from flask import current_app

from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt import JWT
from flask_redis import FlaskRedis
from raven.contrib.flask import Sentry
from slackclient import SlackClient

from application.services.theme import _reload_template, _get_template_name


sc = SlackClient("xoxb-68385490752-9gPeX5F6krKS84C1LO6moByC")
jwt = JWT()
mail = Mail()
admin = Admin()
redis = FlaskRedis()
login_manager = LoginManager()
sentry = Sentry()
