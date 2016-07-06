#!/usr/bin/env python
# encoding: utf-8
import json

from flask import Blueprint, current_app, jsonify, request
from flask_jwt import jwt_required
from voluptuous import MultipleInvalid

from application.models import Category, Permission, Post, Tag
from application.utils.permission import permission_required
from application.utils.response import make_error_resp, normal_resp, page_resp
from application.utils.saver import (save_model_from_json,
                                     update_model_from_json)
from application.utils.validator import post_schema, post_update_schema

post_bp = Blueprint('posts', __name__, url_prefix='/posts')


@post_bp.route('/all', methods=['GET'])
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
def all_categories():
    """query all categories"""
    cates = Category.objects.all()
    return normal_resp({'categories': [cate.to_json() for cate in cates]})


@post_bp.route('/post', methods=['GET'])
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
@jwt_required()
@permission_required(Permission.CREATE)
def add_post():
    """add post to db"""
    data = request.get_json()
    try:
        post = post_schema(data)
    except MultipleInvalid as e:
        return make_error_resp(2001, str(e))
    # user = User.objects.get_by_id(str(current_identity.id))
    current_app.logger.debug("save post with categories: {}".format(post.get('categories')))
    status, obj = save_model_from_json(Post, post)
    current_app.logger.debug("post errors: {}".format(obj))
    if status:
        return normal_resp({'post': obj.to_json()})
    else:
        return make_error_resp(2001, {})


@post_bp.route('/post', methods=['PUT'])
@jwt_required()
@permission_required(Permission.UPDATE)
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
        return normal_resp({'post': db_post.to_json()})
    else:
        return make_error_resp(2001, 'arg errors')


@post_bp.route('/post', methods=['DELETE'])
@jwt_required()
@permission_required(Permission.DELETE)
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
