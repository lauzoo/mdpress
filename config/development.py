# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    """Base config class."""
    TESTING = False
    SECRET_KEY = "DevelopmentConfig"
    JWT_AUTH_USERNAME_KEY = "username"
    JWT_AUTH_PASSWORD_KEY = "password"

    # Site domain
    SITE_TITLE = "mdpress"

    REDIS_CONFIG = {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 10
    }

    UPLOAD_FOLDER = "/tmp/upload"
