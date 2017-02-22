#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import json
import time
import logging
import logging.handlers
from datetime import datetime

import redisco
from flask import Flask, current_app, request

from config import load_config
from application.extensions import mail, redis, sentry, login_manager
from application.controllers import all_bp
from application.models import User
from application.services.theme import setup_theme

# convert python's encoding to utf8
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    pass


def create_app(mode):
    """Create Flask app."""
    config = load_config(mode)

    template_folder = 'templates/MinimalBox'
    app = Flask(__name__, template_folder=template_folder)
    app.config.from_object(config)

    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing

    # Register components
    configure_logging(app)
    register_blueprint(app)
    register_extensions(app)
    register_tasks(app)
    register_theme(app)

    return app


def register_extensions(app):
    if app.config.get('ELASTICSEARCH_SUPPORT', False):
        es.init_app(app)
    mail.init_app(app)
    redis.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = '/admin/login'
    login_manager.init_app(app)

    """init redis connection"""
    redisco.connection_setup(host=app.config['REDIS_CONFIG']['HOST'],
                             port=app.config['REDIS_CONFIG']['PORT'],
                             db=app.config['REDIS_CONFIG']['DB'])

    def filter_func(kv):
        print(kv)

    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    from application.services.theme import RedisLoader
    app.jinja_env.loader = RedisLoader()

    from pyjade import Compiler
    Compiler.register_autoclosecode('load')

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.get_by_id(user_id)

    if not app.config['DEBUG'] and not app.config['TESTING']:
        sentry.init_app(app, dsn='https://629e0f9d9a0b474585f3355a640ffa99:d0fe041082384cdfab8f0f6d0846e54c@app.getsentry.com/93431')


def register_blueprint(app):
    for bp in all_bp:
        app.register_blueprint(bp)

    @app.before_request
    def log_request():
        req_ip = request.headers.get('X-Real-Ip')
        req_data = {"timestamp": datetime.utcnow(),
                    "ip": req_ip if req_ip else request.remote_addr,
                    "request_method": request.method,
                    "request_url": request.url,
                    "request_path": request.path,
                    "request_data": json.dumps(request.data)}
        for k, v in request.headers.items():
            req_data["request_header_{}".format(k)] = v
        if current_app.config.get('ELASTICSEARCH_SUPPORT'):
            rst = es.index(index="mdpress", doc_type="request_log", body=req_data)
            current_app.logger.info("before reqeust result: {}".format(rst))
        else:
            dt = datetime.now()
            key = "request_log:{}:{}:{}:{}:{}:{}".format(
                dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            redis.hmset(key, req_data)

        if not app.config.get('DEBUG') and not app.config.get('TESTING'):
            from application.tasks.slack import log_request
            log_request.delay(request.path, req_data)

    @app.errorhandler(404)
    def page_not_found(error):
        # req_ip = request.headers.get('X-Real-Ip') or request.remote_addr
        redis.zincrby("mdpress:visit-404", request.path)
        return 'Page Not Found!!!', 404


def register_theme(app):
    theme = app.config.get('THEME', 'default')
    setup_theme(app, theme, True)
    setup_theme(app, 'admin', False)


def configure_logging(app):
    # logging.basicConfig()
    if app.config.get('TESTING'):
        app.logger.setLevel(logging.INFO)
        return
    elif app.config.get('DEBUG'):
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setLevel(logging.DEBUG)
    logging_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(logging_handler)


def register_tasks(app):
    from application.tasks.slack import log_request
