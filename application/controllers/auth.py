#!/usr/bin/env python
# encoding: utf-8
import json

from flask import Blueprint, current_app, request, jsonify
from flask.ext.login import login_user, logout_user

import application.models as Models


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    current_app.logger.debug("login with rdata: {}".format(request.data))
    info = json.loads(request.data)
    username = info.get('username', 'guest@test.com')
    password = info.get('password', '')

    user = Models.User.objects.filter(email=username).first()
    if user and user.password == password:
        login_user(user)
        return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'logout success'}})
