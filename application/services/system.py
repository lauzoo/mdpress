#!/usr/bin/env python
# encoding: utf-8
import os

from flask import current_app as app


def has(temp_name):
    template_path = os.path.join(app.config['PROJECT_PATH'], 'application/templates/MinimalBox')
    file_path = os.path.join(template_path, temp_name)

    ext = file_path[-4:]
    file_path = file_path + '.jade' if ext != 'jade' else file_path
    if os.path.exists(file_path):
        return True

    return False
