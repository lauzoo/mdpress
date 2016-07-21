#!/usr/bin/env python
# encoding: utf-8
import os

from flask import (request, Blueprint, send_from_directory,
                   current_app as app, url_for, render_template)
from scss import Compiler

from application.models import Post
from application.models.system import site
from application.services.system import has

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
    page = request.args.get('page', 1)
    page_size = int(request.args.get('page_size', 5))
    page_size = max([5, min([20, page_size])])
    posts = Post.objects.all()
    show_posts = posts[(page - 1) * page_size:][:page_size]
    for post in show_posts:
        post.date = {
            'format': post.date.strftime
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


@frontend_bp.route('/archive')
def archive():
    def group(self, *args, **kwargs):
        return self

    def get_data(type, sort, limit):
        rst = {}
        posts = Post.objects.all()
        for post in posts:
            post.date = {
                'format': lambda x: post.updated_at.strftime(x),
            }
            post.metadata = {
                'refer': url_for('frontend.post', post_id=post.id),
            }
            year = post.updated_at.strftime('%Y')
            if year in rst:
                rst[year].append(post)
            else:
                rst[year] = [post]
        rtn = []
        for item, value in rst.iteritems():
            rtn.append((item, tuple(value)))
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
