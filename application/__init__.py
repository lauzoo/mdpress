#!/usr/bin/env python
# encoding: utf-8
import sys
import logging
import logging.handlers
from datetime import datetime

import redisco
from flask import Flask, current_app, request, jsonify
from flask_jwt import JWTError

from config import load_config
from application.extensions import jwt
from application.controllers import all_bp

# convert python's encoding to utf8
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    pass


def create_app(mode):
    """Create Flask app."""
    print "mode: {}".format(mode)
    config = load_config(mode)

    app = Flask(__name__)
    app.config.from_object(config)

    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing

    # Register components
    configure_logging(app)
    register_extensions(app)
    register_blueprint(app)

    return app


def register_extensions(app):
    """init redis connection"""
    redisco.connection_setup(host=app.config['REDIS_CONFIG']['HOST'],
                             port=app.config['REDIS_CONFIG']['PORT'],
                             db=app.config['REDIS_CONFIG']['DB'])
    # jwt config
    def jwt_authenticate(email, password):
        logging.info("email:{}\npassword:{}\n".format(email, password))
        from application.models import User
        user = User.objects.filter(email=email).first()
        if user and user.password==password:
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


def configure_logging(app):
    logging.basicConfig()
    if app.config.get('TESTING'):
        app.logger.setLevel(logging.CRITICAL)
        return
    elif app.config.get('DEBUG'):
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # info_log = os.path.join("running-info.log")
    info_log = "/tmp/logs/running.info"
    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log, maxBytes=104857600, backupCount=10)
    info_file_handler.setLevel(logging.DEBUG)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)
