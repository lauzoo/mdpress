#!/usr/bin/env python
# encoding: utf-8
import json

from flask import flash, redirect, url_for, Blueprint, current_app, request
from flask_login import login_user, logout_user, login_required

import application.models as Models

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    info = current_app.logger.info
    current_app.logger.debug("login with rdata: {}".format(request.data))
    username = request.form.get('username', 'guest@test.com')
    info(username)
    password = request.form.get('password', '')
    info(password)

    user = Models.User.objects.filter(email=username).first()
    if user and user.password == password:
        login_user(user)
        return redirect(url_for('admin.index'))
    else:
        flash("Username Not Exists")
        return redirect(url_for('admin.login'))


@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
