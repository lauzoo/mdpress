#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    return render_template('index.html')


@frontend_bp.route('/test')
def test():
    return render_template('test.html')
