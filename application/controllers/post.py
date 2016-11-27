#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from flask import Blueprint, current_app, request
from voluptuous import MultipleInvalid
from flask_login import login_required, current_user

from application.models import Category, Post
from application.utils.response import make_error_resp, normal_resp, page_resp
from application.utils.saver import (save_model_from_json,
                                     update_model_from_json)
from application.utils.template import format_markdown
from application.utils.validator import post_schema, post_update_schema

post_bp = Blueprint('posts', __name__, url_prefix='/posts')


@post_bp.route('/all', methods=['GET'])
@login_required
def all_post():
    """query all posts"""
    page = request.args.get('page', 1)
    page_size = request.args.get('pagesize', 10)
    ps = Post.objects.all()
    total = len(ps)
    ps = ps[page_size * (page - 1): page_size * page]
    return page_resp({'posts': [p.to_json() for p in ps]},
                     total, page, page_size)


@post_bp.route('/all_categories', methods=['GET'])
@login_required
def all_categories():
    """query all categories"""
    cates = Category.objects.all()
    return normal_resp({'categories': [cate.to_json() for cate in cates]})


@post_bp.route('/post', methods=['GET'])
@login_required
def qry_post():
    """query post with post id"""
    id = request.args.get('id')
    if not id:
        return make_error_resp(2001, 'id not found')
    current_app.logger.debug("post id :{}".format(id))
    post = Post.objects.get_by_id(id)
    if not post:
        return make_error_resp(2002, 'post not found')
    else:
        return normal_resp({'post': post.to_json()})


@post_bp.route('/post', methods=['POST'])
@login_required
def add_post():
    """add post to db"""
    data = request.get_json()
    try:
        post = post_schema(data)
    except MultipleInvalid as e:
        return make_error_resp(2001, str(e))
    current_app.logger.debug("save post with categories: {}".format(post.get('categories')))
    status, obj = save_model_from_json(Post, post)
    current_app.logger.debug("post status: {}".format(status))
    if status:
        obj.content = format_markdown(obj.markdown)
        obj.published_at = datetime.now()
        obj.created_at = datetime.now()
        obj.author = current_user._get_current_object()
        current_app.logger.info("save post with len: {}".format(len(obj.content)))
        obj.save()
        return normal_resp({'post': obj.to_json()})
    else:
        return make_error_resp(2001, {})


@post_bp.route('/post', methods=['PUT'])
@login_required
def udt_post():
    post = request.get_json()
    try:
        post = post_update_schema(post)
    except MultipleInvalid as e:
        return make_error_resp(2001, str(e))

    db_post = Post.objects.get_by_id(post.get('id'))
    if not db_post:
        return make_error_resp(2001, 'post not found in db')
    status, obj = update_model_from_json(db_post, post)
    if status:
        obj.content = format_markdown(obj.markdown)
        obj.author = current_user._get_current_object()
        obj.updated_at = datetime.now()
        current_app.logger.info("save post with len: {}".format(len(obj.content)))
        obj.save()
        return normal_resp({'post': db_post.to_json()})
    else:
        return make_error_resp(2001, 'arg errors')


@post_bp.route('/post', methods=['DELETE'])
@login_required
def del_post():
    ids = request.get_json().get('ids')
    if not ids:
        return make_error_resp(2001, 'id not found')
    current_app.logger.debug("delete post id :{}".format(ids))
    uids = set(ids)
    posts = []
    for id in uids:
        post = Post.objects.get_by_id(id)
        if post:
            posts.append(post)
    if not posts:
        return make_error_resp(2002, 'posts not found')
    else:
        data = [p.to_json() for p in posts]
        for p in posts:
            p.delete()
        return normal_resp({'success': len(posts), 'total': len(ids),
                            'posts': data})
