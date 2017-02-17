# coding: utf-8
import os
from datetime import timedelta


class Config(object):
    """Base config class."""
    # Flask app config
    DEBUG = True
    TESTING = False
    SECRET_KEY = "sample_key"

    # Template Theme
    THEME = "MinimalBox"
    THEME_KEY = "mdpress:theme"
    TEMPLATE_PREFIX = "mdpress:template:theme"
    AUTO_RELOAD_TEMPLATE = True

    # JWT SETTING
    JWT_AUTH_URL_RULE = "/authentication/token"
    JWT_AUTH_USERNAME_KEY = "username"
    JWT_AUTH_PASSWORD_KEY = "password"
    JWT_AUTH_HEADER_PREFIX = "Bearer"
    JWT_EXPIRATION_DELTA = timedelta(days=1)

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Site domain
    SITE_DOMAIN = "http://localhost:8080"

    # redis config
    REDIS_URL = "redis://:@localhost:6379/0"
    REDIS_CONFIG = {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 10
    }

    # mail
    MAIL_SERVER = "you smtp server"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "your email"
    MAIL_PASSWORD = "your email password"

    # code highlight style
    HIGHLIGHT_STYLE = "vim"

    # slack
    SLACK_BOT_TOKEN = "abcd"

    # upload
    UPLOAD_FOLDER = "/usr/local/upload"
    CLOUD_UPLOAD_SITE = "smms"
    CLOUD_UPLOAD_CONFIG = {
        "url": "https://sm.ms/api/upload"
    }
