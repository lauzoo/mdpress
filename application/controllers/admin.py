#!/usr/bin/env python
# encoding: utf-8
from flask import request, render_template, Blueprint

import application.models as Models
from application.utils import Pagination


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@admin_bp.route('/posts', methods=['GET'])
def all_posts():
    posts = Models.Post.objects.all()
    page = Pagination(posts)
    return render_template('post-list.html', page=page)


@admin_bp.route('/posts/oper', methods=['GET'])
def oper_post():
    id = request.args.get('pid')
    if id:
        post = Models.Post.objects.get_by_id(id)
        return render_template('add-new.html', post=post)
    return render_template('add-new.html')


@admin_bp.route('/tags', methods=['GET'])
def all_tags():
    return render_template('tag-list.html')


@admin_bp.route('/uploads', methods=['GET'])
def all_uploads():
    return render_template('upload-list.html')


@admin_bp.route('/comments', methods=['GET'])
def all_comments():
    return render_template('comment-list.html')


@admin_bp.route('/settings', methods=['GET'])
def settings():
    return render_template('profile.html')


@admin_bp.route('/other', methods=['GET'])
def other():
    pass
