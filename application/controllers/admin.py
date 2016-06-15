#!/usr/bin/env python
# encoding: utf-8
from flask import render_template, Blueprint


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@admin_bp.route('/posts', methods=['GET'])
def all_posts():
    return render_template('post-list.html')


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
