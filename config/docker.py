# coding: utf-8
from .default import Config


class DockerConfig(Config):
    """Base config class."""
    TESTING = False
    SECRET_KEY = "DockerConfig"

    # Site domain
    SITE_TITLE = "mdpress"

    REDIS_CONFIG = {
        'HOST': '192.168.59.103',
        'PORT': 26379,
        'DB': 7
    }

    UPLOAD_FOLDER = "/tmp/upload"
