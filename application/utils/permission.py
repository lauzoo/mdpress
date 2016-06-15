#!/usr/bin/env python
# encoding: utf-8
from functools import wraps

from flask import jsonify
from flask_jwt import current_identity


def create_response_with(code, msg):
    resp = {
        'data': {},
        'msg': msg,
        'code': code,
        'extra': {}
    }
    return jsonify(**resp)


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_identity.is_authenticated:
                return create_response_with(2001, 'need login')
            user_roles = current_identity.role
            print "need_permission: {0:b} has_permission: {0:b}".format(permission, user_roles)
            for role in user_roles:
                user_permission = role.permission
                if user_permission & permission == permission:
                    return func(*args, **kwargs)
            else:
                print "user has no permission"
                return create_response_with(2009, 'no permission')
        return decorated_function
    return decorator
