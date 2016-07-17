#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from flask import request, Blueprint, render_template

from application.models import Post

frontend_bp = Blueprint('frontend', __name__)


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
        post.content = {
            'limit': lambda x: post.cnt[0:x]
        }
    env = {
        'site': {
            'title': 'Hello'
        },
        'has': lambda x: False,
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
    return render_template('archive.jade', **env)


@frontend_bp.route('/post/<post_id>')
def post(post_id):
    return render_template('post.jade', post=post)
