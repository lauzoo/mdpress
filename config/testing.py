# coding: utf-8
from .default import Config


class TestingConfig(Config):
    """Base config class."""
    TESTING = True
    SECRET_KEY = "DevelopmentConfig"

    # Site domain
    SITE_TITLE = "mdpress"

    REDIS_CONFIG = {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 8
    }

    UPLOAD_FOLDER = "/tmp/upload"
