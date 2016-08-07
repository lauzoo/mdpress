# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    """Base config class."""
    TESTING = False
    SECRET_KEY = "DevelopmentConfig"

    # Site domain
    SITE_TITLE = "mdpress"

    REDIS_CONFIG = {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 10
    }

    UPLOAD_FOLDER = "/tmp/upload"

    # elastic search support
    ELASTICSEARCH_SUPPORT = True
    ELASTICSEARCH_HOST = "127.0.0.1:9200"
