#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    return render_template('index.html')


@frontend_bp.route('/test')
def test():
    env = {
        'site': {
            'title': 'Hello'
        },
        'has': lambda x: False,
        'paginator': {
            'has_pre': True,
            'has_next': True,
        },
        'pager': {
            'pre_url': '',
            'next_url': ''
        },
    }
    return render_template('index.jade', **env)
