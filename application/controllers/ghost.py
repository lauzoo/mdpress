#!/usr/bin/env python
# encoding: utf-8
import json

from flask import Blueprint, request, jsonify, current_app
from flask_jwt import jwt_required, current_identity

import application.models as Models
from application.utils import get_slug_id
from application.utils.saver import save_model_from_json, update_model_from_json


ghost_bp = Blueprint('ghost', __name__)


@ghost_bp.route('/posts/', methods=['GET'])
def query_posts():
    """query all posts"""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pagesize', 10))
    ps = Models.Post.objects.filter()
    ps = ps[page_size * (page - 1): page_size * page]
    resp = {
        'posts': [p.to_json() for p in ps],
    }
    return jsonify(**resp)


@ghost_bp.route('/posts/', methods=['POST'])
def add_post():
    posts = request.get_json()['posts']
    result = []
    for post in posts:
        result.append(save_model_from_json(Models.Post, post))
    return jsonify({'posts': posts})


@ghost_bp.route('/posts/', methods=['PUT'])
def update_post():
    new_posts = json.loads(request.data).get('posts')
    for post in new_posts:
        pass
    resp = {'posts': [new_posts]}

    return jsonify(**resp)


@ghost_bp.route('/posts/<id>/', methods=['GET'])
def query_post_by_id(id):
    post = Models.Post.objects.get_by_id(id)
    return jsonify(**{'posts': [post.to_json()]})


@ghost_bp.route('/posts/<id>/', methods=['PUT'])
def update_post_by_id(id):
    post = Models.Post.objects.get_by_id(id)
    new_post = request.get_json()['posts'][0]
    update_model_from_json(post, new_post)
    return jsonify(**{'posts': [post.to_json()]})


@ghost_bp.route('/posts/slug/<slug>', methods=['GET'])
def query_post_by_slug(slug):
    pass


@ghost_bp.route('/tags/', methods=['GET'])
def query_tags():
    tags = Models.Tag.objects.all()
    rsp = {
        "tags": [tag.to_json() for tag in tags],
        "meta": {
            "pagination": {
                "page": 1, "limit": "all", "pages": 1, "total": len(tags),
                "next": None, "prev": None
            }
        }
    }
    return jsonify(**rsp)


@ghost_bp.route('/tags/<id>', methods=['GET'])
def query_tag_by_id(id):
    tag = Models.Tag.objects.get_by_id(id)
    rsp = {
        "tags": [tag.to_json()],
    }
    return jsonify(**rsp)


@ghost_bp.route('/tags/slug/<slug>/', methods=['GET'])
def query_tag_by_slug(slug):
    tag = Models.Tag.objects.filter(slug=slug).first()
    rsp = {
        "tags": [tag.to_json() if tag else {}],
    }
    return jsonify(**rsp)


@ghost_bp.route('/slugs/post/<slug>/')
def query_slug_for_post(slug):
    post = Models.Post.objects.filter(slug=slug).first()
    if post:
        slug = slug + "-{}".format(get_slug_id())
    return jsonify(**{"slugs": [{"slug": slug}]})


@ghost_bp.route('/users/', methods=['GET'])
def query_users():
    users = Models.User.objects.all()
    rsp = {
        "users": [user.to_json() for user in users],
        "meta": {
            "pagination": {
                "page": 1, "limit": "all", "pages": 1, "total": len(users),
                "next": None, "prev": None
            }
        }
    }
    return jsonify(**rsp)


@ghost_bp.route('/users/<id>', methods=['GET'])
def query_user_by_id(id):
    pass


@ghost_bp.route('/users/slug/<slug>', methods=['GET'])
def query_user_by_slug(slug):
    pass


@ghost_bp.route('/users/email/<email>', methods=['GET'])
def query_user_by_email(email):
    pass


@ghost_bp.route('/settings/', methods=['GET'])
def settings():
    with open('utils/ghost/settings.json', 'r') as f:
        data = f.read()
    resp = json.loads(data)
    return jsonify(**resp)


@ghost_bp.route('/users/<user>/', methods=['GET'])
@jwt_required()
def query_user(user):
    if user == 'me':
        user = current_identity
    else:
        user = Models.User.objects.get_by_id(user)
    resp = {
        "users": [user.to_json()],
    }
    return jsonify(**resp)


@ghost_bp.route('/notifications/', methods=['GET'])
def notifications():
    return jsonify(**{"notifications": []})


