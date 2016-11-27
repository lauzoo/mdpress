#!/usr/bin/env python
# encoding: utf-8
from flask import (request, Blueprint, send_from_directory,
                   current_app as app, url_for, abort, redirect)


callback_bp = Blueprint('callback', __name__, '/callback')


@callback_bp.route('duoshuo', methods=['POST'])
def duoshuo_callback():
    pass
