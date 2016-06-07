#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from flask import request, jsonify, current_app, Blueprint
from flask_jwt import jwt_required, current_identity

import application.models as Models
from application.utils.validator import post_schema
from application.utils.generator import generator_post_id


post_bp = Blueprint('posts', __name__, url_prefix='/posts')


@post_bp.route('/all', methods=['GET'])
def all_post():
    """query all posts"""
    page = request.args.get('page', 1)
    page_size = request.args.get('pagesize', 10)
    ps = Models.Post.objects.filter()
    total = len(ps)
    ps = ps[page_size * (page - 1): page_size * page]
    resp = {
        'data': {'total': total,
                 'posts': [p.to_json() for p in ps],
                 'page': page,
                 'page_size': page_size},
        'msg': 'success',
        'code': 2000,
        'extra': {}
    }
    return jsonify(**resp)


@post_bp.route('/post', methods=['GET'])
def qry_post():
    """query post with post id"""
    id = request.args.get('id')
    if not id:
        resp = {
            'data': {},
            'msg': 'id not found',
            'code': 2001,
            'extra': {}
        }
    current_app.logger.info("post id :{}".format(id))
    post = Models.Post.objects.filter(id=id).first()
    if not post:
        resp = {
            'data': {},
            'msg': 'post not found',
            'code': 2002,
            'extra': {}
        }
    else:
        resp = {
            'data': post.to_json(),
            'msg': '',
            'code': 2000,
            'extra': {}
        }
    return jsonify(**resp)


@post_bp.route('/post', methods=['POST'])
@jwt_required()
def add_post():
    """add post to db"""
    data = request.get_json()
    post = post_schema(data)
    post = Models.Post(
        id=generator_post_id(), title=post.get('title'), create_at=datetime.now(),
        excerpt=post.get('excerpt'), content=post.get('content'),
        user=int(current_identity.id), categories=post.get('categories'),
        tags=post.get('tags'), status=post.get('status'))
    status = post.save()
    current_app.logger.info("save post with status: {}".format(status))
    post = Models.Post.objects.filter(id=post.id).first()
    current_app.logger.info("post create at: {}".format(post.create_at))
    return jsonify(**post.to_json())


@post_bp.route('/post', methods=['PUT'])
@jwt_required()
def udt_post():
    pass


@post_bp.route('/post', methods=['DELETE'])
@jwt_required()
def del_post():
    ids = request.get_json().get('ids')
    if not ids:
        resp = {
            'data': {},
            'msg': 'id not found',
            'code': 2001,
            'extra': {}
        }
    current_app.logger.info("delete post id :{}".format(ids))
    uids = set(ids)
    posts = []
    for id in uids:
        post = Models.Post.objects.filter(id=id).first()
        if post:
            posts.append(post)
    if not posts:
        resp = {
            'data': {'post_ids': [id for id in ids]},
            'msg': 'posts not found',
            'code': 2002,
            'extra': {}
        }
    else:
        resp = {
            'data': {
                'success': len(posts),
                'total': len(ids),
                'posts': [p.to_json() for p in posts]
            },
            'msg': 'success',
            'code': 2000,
            'extra': {}
        }
        for p in posts:
            p.delete()
    return jsonify(**resp)
