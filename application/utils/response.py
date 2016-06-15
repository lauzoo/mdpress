#!/usr/bin/env python
# encoding: utf-8
from flask import jsonify


def make_error_resp(code, msg):
    return jsonify(**{
        'data': {},
        'msg': msg,
        'code': code,
        'extras': {}
    })


def normal_resp(data):
    return jsonify(**{
        'data': data,
        'msg': 'success',
        'code': 2000,
        'extras': {}
    })


def page_resp(data, total, page, page_size):
    resp = {
        'data': data,
        'msg': 'success',
        'code': 2000,
        'extras': {
            'total': total,
            'page': page,
            'page_size': page_size,
            'has_prev': page > 1,
            'has_next': (page_size) * page < total
        },
    }
    return jsonify(**resp)
