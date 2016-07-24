#!/usr/bin/env python
# encoding: utf-8
import os
from functools import partial

from flask import (request, Blueprint, send_from_directory,
                   current_app as app, url_for, render_template)
from scss import Compiler

from application.models import Post
from application.models.system import site
from application.services.system import has

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 20
frontend_bp = Blueprint('frontend', __name__)
base_env = {
    'site': site,
    'has': has,
    'paginator': {
        'has_pre': False,
        'has_next': False,
    },
    'pager': {
        'pre_url': '',
        'next_url': ''
    },
}


@frontend_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', DEFAULT_PAGE)
    page_size = int(request.args.get('page_size',
                                     DEFAULT_PAGE_SIZE))
    page_size = max([DEFAULT_PAGE_SIZE, min([MAX_PAGE_SIZE, page_size])])
    posts = Post.objects.all()
    show_posts = posts[(page - 1) * page_size:][:page_size]
    for post in show_posts:
        post.published_at = {
            'format': post.published_at.strftime
        }
        post.cnt = post.content
        post.content = post.cnt[0:100]
        post.metadata = {
            'refer': url_for('frontend.post', post_id=post.id)
        }
    env = {
        'site': site,
        'has': has,
        'paginator': {
            'has_pre': page > 1,
            'has_next': page * page_size < len(posts),
        },
        'pager': {
            'pre_url': '',
            'next_url': ''
        },
        'posts': show_posts,
    }
    return render_template('index.jade', **env)


def format(d, f):
    return d.strftime(f)


@frontend_bp.route('/archive')
def archive():
    def group(self, *args, **kwargs):
        return self

    def get_data(type, sort, limit):
        rst = {}
        posts = Post.objects.all().order('-published_at')
        for post in posts:
            d = post.published_at
            post.date = {
                'format': partial(format, d)
            }
            post.metadata = {
                'refer': url_for('frontend.post', post_id=post.id),
            }
            year = d.strftime('%Y')
            if year in rst:
                rst[year].append(post)
            else:
                rst[year] = [post]
        keys = sorted(rst.keys(), reverse=True)
        rtn = [(k, tuple(rst[k])) for k in keys]
        return rtn

    env = {
        'get_data': get_data
    }
    env.update(base_env)

    return render_template('archive.jade', **env)


@frontend_bp.route('/post/<post_id>')
def post(post_id):
    post = Post.objects.get_by_id(post_id)
    if post:
        d = post.date
        post.date = {
            'format': lambda x: d.strftime(x)
        }
    env = {
        'post': post
    }
    env.update(base_env)
    return render_template('post.jade', **env)


@frontend_bp.route('/about')
def about():
    env = {
    }
    env.update(base_env)
    return render_template('about.jade', **env)


@frontend_bp.route('/template/<filename>')
def template_static(filename):
    template_path = os.path.join(app.config['PROJECT_PATH'], 'application/templates/MinimalBox')
    if filename[-4:] == 'scss':
        file_path = os.path.join(template_path, filename)
        filename = "{}{}".format(filename[:-4], "css")
        with open(os.path.join(template_path, filename), 'w') as f:
            f.write(Compiler().compile(file_path))

    # todo: danguage function
    return send_from_directory(template_path, filename)
