# coding: utf-8
from .default import Config


class TestingConfig(Config):
    """Base config class."""
    TESTING = True
    SECRET_KEY = "DevelopmentConfig"

    # Site domain
    SITE_TITLE = "mdpress"

    REDIS_CONFIG = {
        'HOST': '192.168.59.103',
        'PORT': 26379,
        'DB': 8
    }

    UPLOAD_FOLDER = "/tmp/upload"
