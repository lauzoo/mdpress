#!/usr/bin/env python
# encoding: utf-8
from flask import render_template


def render_theme_template(template, **kwargs):
    return render_template(template, **kwargs)
