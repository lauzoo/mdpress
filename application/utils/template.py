#!/usr/bin/env python
# encoding: utf-8
from flask import current_app, render_template

from application.extensions import redis

def render_theme_template(template, **kwargs):
    return render_template(template, **kwargs)
