#!/usr/bin/env python
# encoding: utf-8
import os
import time

from redis import Redis
from flask import current_app
from jinja2 import BaseLoader, TemplateNotFound


class RedisLoader(BaseLoader):
    def __init__(self):
        self.redis = Redis('127.0.0.1', 6379)

    def get_source(self, environment, template):
        current_app.logger.debug("load template: {}".format(template))
        template_prefix = current_app.config.get('TEMPLATE_PREFIX')
        if template[:6] == "admin/":
            key = "{prefix}:{theme}:{file}".format(
                prefix=template_prefix, theme='admin',
                file=_get_template_name(template))
        else:
            theme = self.redis.get(current_app.config.get('THEME_KEY'))
            key = "{prefix}:{theme}:{file}".format(
                prefix=template_prefix, theme=theme,
                file=template)

        if current_app.config.get('AUTO_RELOAD_TEMPLATE'):
            _reload_template(current_app, key)

        temp = self.redis.get("{}:content".format(key))
        return temp, key, lambda: False

def _get_filenames(filename):
    raw_filenames = filename.split('+')
    rst = []
    file_type = '.jade'
    if filename.find('.') != -1:
        file_type = filename[filename.find('.'):]
    for name in raw_filenames:
        if name.find(file_type) == -1:
            rst.append('{}{}'.format(name, file_type))
        else:
            rst.append(name)
    return rst

def setup_theme(app, theme, change_theme=False):
    from application.extensions import redis
    theme_key = app.config.get('THEME_KEY')
    if change_theme:
        redis.set(theme_key, theme)

    template_prefix = app.config.get('TEMPLATE_PREFIX')
    template_path = os.path.join(app.config['PROJECT_PATH'],
                                 'application/templates', theme)

    # add theme file
    for rt, _, fs in os.walk(template_path):
        for f in fs:
            for filename in _get_filenames(f):
                full_path = os.path.join(rt, filename)
                filename = full_path[len(template_path)+1:]
                path = os.path.join(rt, f)
                if os.path.isfile(path):
                    with open(path, 'r') as fp:
                        data = fp.read()
                        key = "{prefix}:{theme}:{filename}".format(
                            prefix=template_prefix, theme=theme,
                            filename=filename)
                        lm_key = "{}:lm".format(key)
                        path_key = "{}:path".format(key)
                        last_modified = time.ctime(os.path.getmtime(path))
                        redis.set("{}:content".format(key), data)
                        redis.set(lm_key, last_modified)
                        redis.set(path_key, path)
                else:
                    app.logger.info("{} is not a file".format(f))


def _reload_template(app, key):
    from application.extensions import redis
    lm_key = "{}:lm".format(key)
    path_key = "{}:path".format(key)

    path = redis.get(path_key)
    last_modified = redis.get(lm_key)

    if not path or not last_modified:
        app.logger.error("template path: {}".format(path))
        app.logger.error("template last modified: {}".format(last_modified))
        raise TemplateNotFound(key)
    curr_last_modified = time.ctime(os.path.getmtime(path))
    if last_modified != curr_last_modified:
        with open(path, 'r') as f:
            data = f.read()
            redis.set(key, data)
            redis.set(lm_key, curr_last_modified)


def _get_template_name(template):
    split_idx = template.find('/')
    if split_idx != -1:
        return template[split_idx + 1:]
    return template

