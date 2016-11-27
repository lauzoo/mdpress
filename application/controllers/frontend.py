#!/usr/bin/env python
# encoding: utf-8
import os
from functools import partial

from flask import (request, Blueprint, send_from_directory,
                   current_app as app, url_for, abort, redirect)
from scss import Compiler

from application.models import Post, Category, POST_STATUS
from application.extensions import redis
from application.utils.template import render_theme_template as render_template
from application.services.search import search as search_srv


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 20
frontend_bp = Blueprint('frontend', __name__)


def get_data(type, sort, limit, status=None, with_page=False):
    if status == 'pages':
        return []
    rst = {}
    posts = Post.objects.all().order('-published_at')
    default_category = Category.objects.filter(name="Default").first()
    for post in posts:
        d = post.created_at
        post.date = {
            'format': partial(format, d)
        }
        post.metadata = {
            'refer': url_for('frontend.post', post_id=post.id),
        }
        if not post.categories:
            post.categories = [default_category]
            post.save()
        for cate in post.categories:
            if cate.name in rst:
                rst[cate.name].append(post)
            else:
                rst[cate.name] = [post]
    # keys = sorted(rst.keys(), reverse=True)
    rtn = [(k, tuple(rst[k])) for k in rst.keys()]
    return rtn

@frontend_bp.route('/', methods=['GET'])
def index():
    try:
        page = int(request.args.get('page', DEFAULT_PAGE))
        page_size = int(request.args.get('page_size',
                                         DEFAULT_PAGE_SIZE))
        page_size = max([DEFAULT_PAGE_SIZE, min([MAX_PAGE_SIZE, page_size])])
    except Exception:
        return abort(404)
    posts = Post.objects.filter(status=POST_STATUS[0]).all().order('-published_at')
    show_posts = posts[(page - 1) * page_size:][:page_size]
    for post in show_posts:
        d = post.created_at
        cnt = post.content
        post.published_at = {
            'format': post.published_at.strftime
        }
        post.date = {
            'format': partial(format, d)
        }
        post.cnt = post.content
        post.content = {
            'limit': lambda x: cnt[:x],
            '__repr__': post.cnt,
        }
        post.metadata = {
            'refer': url_for('frontend.post', post_id=post.slug)
        }
    env = {
        'paginator': {
            'has_pre': page > 1,
            'has_next': page * page_size < len(posts),
        },
        'pager': {
            'has_pre': page > 1,
            'has_next': page * page_size < len(posts),
            'pre_url': url_for('frontend.index', page=page - 1),
            'next_url': url_for('frontend.index', page=page + 1)
        },
        'get_data': get_data,
        'posts': show_posts,
    }
    return render_template('index.jade', **env)


def format(d, f):
    return d.strftime(f)


@frontend_bp.route('/archive')
def archive():
    def group(self, *args, **kwargs):
        return self

    def get_data(type, sort, limit, status=None, with_page=False):
        if status == 'pages':
            return []
        rst = {}
        posts = Post.objects.filter(status=POST_STATUS[0]).order('-published_at')
        default_category = Category.objects.filter(name="Default").first()
        for post in posts:
            d = post.created_at
            post.date = {
                'format': partial(format, d)
            }
            post.metadata = {
                'refer': url_for('frontend.post', post_id=post.id),
            }
            if not post.categories:
                post.categories = [default_category]
                post.save()
            for cate in post.categories:
                if cate.name in rst:
                    rst[cate.name].append(post)
                else:
                    rst[cate.name] = [post]
        # keys = sorted(rst.keys(), reverse=True)
        rtn = [(k, tuple(rst[k])) for k in rst.keys()]
        return rtn

    env = {
        'get_data': get_data,
        'paginator': {
            'has_pre': False,
            'has_next': False,
        },
        'pager': {
            'pre_url': '',
            'next_url': ''
        },
    }

    return render_template('archive.jade', **env)


@frontend_bp.route('/<post_id>')
@frontend_bp.route('/<post_id>/')
@frontend_bp.route('/post/<post_id>')
@frontend_bp.route('/post/<post_id>/')
def post(post_id):
    if post_id.isdigit():
        post = Post.objects.get_by_id(int(post_id))
    else:
        post = Post.objects.filter(slug=post_id.strip()).first()

    if not post or post.status != POST_STATUS[0]:
        return redirect(url_for('frontend.index'))

    if post.posts_count:
        post.posts_count = str(int(post.posts_count) + 1)
    else:
        post.posts_count = '1'
    post.save()
    d = post.published_at
    post.date = {
        'format': lambda x: d.strftime(x)
    }
    env = {
        'post': post,
        'get_data': get_data,
    }
    return render_template('post.jade', **env)

@frontend_bp.route('/page/<page_id>')
@frontend_bp.route('/page/<page_id>/')
def wp_page(page_id):
    return redirect(url_for('frontend.index', page=page_id))


@frontend_bp.route('/<year>/<month>')
@frontend_bp.route('/<year>/<month>/')
def year_month_posts(year, month):
    try:
        page = int(request.args.get('page', DEFAULT_PAGE))
        page_size = int(request.args.get('page_size',
                                         DEFAULT_PAGE_SIZE))
        page_size = max([DEFAULT_PAGE_SIZE, min([MAX_PAGE_SIZE, page_size])])
    except Exception:
        return abort(404)
    posts = Post.objects.filter(status=POST_STATUS[0]).all().order('-published_at')
    show_posts = posts[(page - 1) * page_size:][:page_size]
    for post in show_posts:
        post.published_at = {
            'format': post.published_at.strftime
        }
        post.cnt = post.content
        post.content = post.cnt[0:100]
        post.metadata = {
            'refer': url_for('frontend.post', post_id=post.slug)
        }
    env = {
        'get_data': get_data,
        'paginator': {
            'has_pre': page > 1,
            'has_next': page * page_size < len(posts),
        },
        'pager': {
            'has_pre': page > 1,
            'has_next': page * page_size < len(posts),
            'pre_url': url_for('frontend.index', page=page - 1),
            'next_url': url_for('frontend.index', page=page + 1)
        },
        'posts': show_posts,
    }
    return render_template('index.jade', **env)


@frontend_bp.route('/about')
def about():
    return redirect('/other/about.html')


@frontend_bp.route('/serach')
def search():
    query_str = request.args.get('q')
    print "query string: {}".format(query_str)
    posts = search_srv(query_str)
    print "posts len: {}".format(len(posts))
    return render_template('search_result.jade', posts=posts)


@frontend_bp.route('/template/<filename>')
def template_static(filename):
    template_path = os.path.join(
        app.config['PROJECT_PATH'],
        'application/templates/{}'.format(redis.get(app.config.get('THEME_KEY'))))
    if filename[-4:] == 'scss':
        file_path = os.path.join(template_path, filename)
        print "file_path: {}".format(file_path)
        filename = "{}{}".format(filename[:-4], "css")
        full_path = os.path.join(template_path, filename)
        if not os.path.exists(file_path):
            abort(404)
        with open(full_path, 'w') as f:
            f.write(Compiler().compile(file_path))
        return send_from_directory(template_path, filename)
    else:
        abort(404)
