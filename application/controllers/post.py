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
    ps = Models.Post.objects.filter()[page_size * (page - 1): page_size * page]
    return jsonify({'posts': [p.to_json() for p in ps]})


@post_bp.route('/post', methods=['GET'])
def qry_post():
    """query post with post id"""
    pass


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
    pass
