#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import logging
import logging.handlers
from datetime import datetime

import jinja2
import redisco
from flask import Flask, current_app, jsonify

from config import load_config
from application.extensions import jwt, mail, redis, RedisLoader
from application.controllers import all_bp

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
    register_extensions(app)
    register_blueprint(app)

    return app


def register_extensions(app):
    mail.init_app(app)
    redis.init_app(app)
    """init redis connection"""
    redisco.connection_setup(host=app.config['REDIS_CONFIG']['HOST'],
                             port=app.config['REDIS_CONFIG']['PORT'],
                             db=app.config['REDIS_CONFIG']['DB'])

    def filter_func(kv):
        print kv

    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    app.jinja_env.loader = RedisLoader()

    from pyjade import Compiler
    Compiler.register_autoclosecode('load')

    # jwt config
    def jwt_authenticate(email, password):
        logging.info("email:{}\npassword:{}\n".format(email, password))
        from application.models import User
        user = User.objects.filter(email=email).first()
        if user and user.password == password:
            return user
        else:
            return None

    def jwt_identity(payload):
        logging.info("payload:{}".format(payload))
        from application.models import User
        user_id = payload['identity']
        return User.objects.get_by_id(user_id)

    def make_payload(identity):
        iat = datetime.utcnow()
        exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
        identity = str(identity.id)
        return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

    def response_handler(access_token, identity):
        return jsonify({'access_token': access_token.decode('utf-8'),
                        'refresh_token': access_token.decode('utf-8'),
                        'expires_in': 24 * 60 * 60,
                        'token_type': 'Bearer'})

    jwt.authentication_handler(jwt_authenticate)
    jwt.identity_handler(jwt_identity)
    jwt.jwt_payload_handler(make_payload)
    jwt.auth_response_handler(response_handler)

    jwt.init_app(app)


def register_blueprint(app):
    for bp in all_bp:
        app.register_blueprint(bp)

    @app.before_first_request
    def setup_templates():
        theme = current_app.config.get('THEME', 'default')
        theme_key = current_app.config.get('THEME_KEY')
        redis.set(theme_key, theme)

        template_prefix = current_app.config.get('TEMPLATE_PREFIX')
        template_path = os.path.join(current_app.config['PROJECT_PATH'],
                                     'application/templates')

        # add theme file
        for rt, _, fs in os.walk(template_path):
            for f in fs:
                path = os.path.join(rt, f)
                postfix = path[len(template_path) + 1:]
                if os.path.isfile(path):
                    with open(path, 'r') as fp:
                        data = fp.read()
                        key = "{}:{}".format(template_prefix, postfix)
                        print key
                        redis.set(key, data)
                else:
                    current_app.logger.info("{} is not a file".format(f))


def configure_logging(app):
    logging.basicConfig()
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
