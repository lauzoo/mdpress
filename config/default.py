# coding: utf-8
import os


class Config(object):
    """Base config class."""
    # Flask app config
    DEBUG = True
    TESTING = True
    SECRET_KEY = "sample_key"
    JWT_AUTH_USERNAME_KEY = "email"
    JWT_AUTH_PASSWORD_KEY = "password"

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Site domain
    SITE_DOMAIN = "http://localhost:8080"
