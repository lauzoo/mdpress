#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template, request
from voluptuous import MultipleInvalid
from flask_login import login_required, current_user

import application.models as Models
from application.models.post import POST_STATUS
from application.utils import Pagination
from application.utils.response import normal_resp, make_error_resp
from application.services.theme import setup_theme
from application.extensions import redis
from application.services.post import build_categories_tree
from application.services.persisten import import_posts, export_posts
from application.utils.validator import system_setting_schema


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET'])
@login_required
def index():
    all_posts = len(Models.Post.objects.all())
    published_posts = len(Models.Post.objects.filter(status=POST_STATUS[0]))
    draft_posts = len(Models.Post.objects.filter(status=POST_STATUS[1]))
    moderate_posts = len(Models.Post.objects.filter(status=POST_STATUS[2]))
    scheduling_posts = len(Models.Post.objects.filter(status=POST_STATUS[3]))

    images = len(Models.Images.objects.all())
    active_images = len(Models.Images.objects.filter(status="active").all())
    return render_template('admin/index.html', user=current_user,
                           postnum={'total': all_posts, 'published': published_posts,
                                    'draft': draft_posts, 'moderate': moderate_posts,
                                    'scheduling': scheduling_posts},
                           imagenum={'total': images, 'active': active_images,
                                     'local': 0, 'remote': images,
                                     'disable': 0})


@admin_bp.route('/login', methods=['GET'])
def login():
    return render_template('admin/login.html')


@admin_bp.route('/posts', methods=['GET'])
@login_required
def all_posts():
    page = int(request.args.get('page', 1))
    posts = Models.Post.objects.order('-published_at').all()
    page = Pagination(posts, page)
    print "has_next: {} pages: {}".format(page.has_next, page.pages)
    return render_template('admin/post-list.html', page=page, user=current_user)


@admin_bp.route('/posts/oper', methods=['GET'])
@login_required
def oper_post():
    id = request.args.get('pid')
    if id:
        post = Models.Post.objects.get_by_id(id)
        return render_template('admin/add-new.html', post=post, user=current_user)
    return render_template('admin/add-new.html', user=current_user)


@admin_bp.route('/tags', methods=['GET', 'POST'])
@login_required
def all_tags():
    if request.method == 'GET':
        return render_template('admin/tag-list.html', user=current_user)
    else:
        tags = [tag.to_json() for tag in Models.Tag.objects.all()]
        rtn = {
            'page': 1,
            'total': len(Models.Tag.objects.all()),
            'rows': [{'id': tag.get('id'),
                      'cell': [tag.get('id'), tag.get('uuid'), tag.get('name'), tag.get('slug'), 0]} for tag in tags]
        }
        return jsonify(rtn)


@admin_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def all_categories():
    if request.method == 'GET':
        cates = [Models.Category.objects.get_by_id(id).to_json() for id in build_categories_tree()]
        return render_template('admin/category-list.html', user=current_user,
                               categories=cates)
    else:
        rtn = {
            'page': 1,
            'total': len(Models.Category.objects.all()),
            'rows': [{'id': cate.get('id'),
                      'cell': [cate.get('id'), cate.get('name'), cate.get('slug'), 0]} for cate in cates]
        }
    return jsonify(rtn)


@admin_bp.route('/categories', methods=['PUT'])
@login_required
def add_category():
    data = request.get_json()
    cate = Models.Category.objects.filter(name=data.get('category')).first()
    if not cate:
        cate = Models.Category.objects.create(name=data.get('category'))
        cate = Models.Category.objects.filter(name=data.get('category')).first()
    return normal_resp({'cate': cate.to_json()})


@admin_bp.route('/gallery', methods=['GET', 'POST'])
@login_required
def all_gallery():
    if request.method == 'GET':
        return render_template('admin/upload-list.html', user=current_user)
    else:
        imgs = [img for img in Models.Images.objects.all()]
        rtn = {
            'page': 1,
            'total': len(Models.Images.objects.all()),
            'rows': [{'id': img.id,
                      'cell': img.to_json()} for img in imgs]
        }
    return jsonify(rtn)


@admin_bp.route('/comments', methods=['GET'])
@login_required
def all_comments():
    return render_template('admin/comment-list.html', user=current_user)


@admin_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('admin/profile.html', user=current_user)


@admin_bp.route('/meta', methods=['GET', 'POST'])
@login_required
def meta():
    if request.method == 'GET':
        tmpls = ["Maupassant", "cais", "classic", "default", "farbtle", "fblog",
                "minimalred", "mo", "shaoyan", "theone", "MinimalBox",
                "twilog", "violet", "writer", "yujian", "yukina"]
        return render_template('admin/options.html', user=current_user,
                            templates=tmpls)
    else:
        try:
            setting = system_setting_schema(request.form)
        except MultipleInvalid as e:
            return make_error_resp(2001, str(e))
        setup_theme(setting.get('theme'))
        return 'ok'


@admin_bp.route('/other', methods=['GET'])
@login_required
def other():
    pass


@admin_bp.route('/import', methods=['GET'])
@login_required
def backup_import():
    import_posts()
    return jsonify(status='ok')


@admin_bp.route('/export', methods=['GET'])
@login_required
def backup_export():
    export_posts()
    return jsonify(status='ok')


@admin_bp.route('/visit_log', methods=['GET'])
@login_required
def visit_log():
    visit_records = []

    today = datetime.now()
    today_records = {'name': u'今日访问',
                     'type': 'line',
                     'stack': u'总量',
                     'data': []
    }
    prefix = "request_log:{}:{}:{}".format(today.year, today.month, today.day)
    for x in xrange(24):
        today_records['data'].append(len(redis.keys(prefix + ":{}:*".format(x))))
    visit_records.append(today_records)

    yesterday = today - timedelta(days=1)
    yesterday_records = {
        'name': u'昨天访问',
        'type': 'line',
        'stack': u'总量',
        'data': []
    }
    prefix = "request_log:{}:{}:{}".format(yesterday.year, yesterday.month, yesterday.day)
    for x in xrange(24):
        yesterday_records['data'].append(len(redis.keys(prefix + ":{}:*".format(x))))
    visit_records.append(yesterday_records)

    last_month = today - timedelta(days=30)
    last_month_records = {
        'name': u'上月平均',
        'type': 'line',
        'stack': u'总量',
        'data': []
    }
    prefix = "request_log:{}:{}:*".format(last_month.year, last_month.month)
    for x in xrange(24):
        last_month_records['data'].append(len(redis.keys(prefix + ":{}:*".format(x))) / 30)
    visit_records.append(last_month_records)
    return jsonify(data=visit_records)
