#!/usr/bin/env python
# encoding: utf-8
import json

from flask import Blueprint, request, jsonify, current_app

import application.models as Models


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
    pass


@ghost_bp.route('/posts/', methods=['PUT'])
def update_post():
    new_post = json.loads(request.data).get('posts')[0]
    with open('utils/ghost/posts.json', 'r') as f:
        data = f.read()
    resp = json.loads(data)
    current_app.logger.info(json.dumps(resp, indent=2))
    current_app.logger.info(json.dumps(new_post, indent=2))
    for idx, post in enumerate(resp['posts']):
        current_app.logger.info(post['slug'])
        current_app.logger.info(new_post['slug'])
        if post['slug'] == new_post['slug']:
            resp['posts'][idx] = new_post
            break
    else:
        new_post = {}
    with open('utils/ghost/posts.json', 'w') as f:
        f.write(json.dumps(resp, indent=2))
    resp = {'posts': [new_post]}

    return jsonify(**resp)


@ghost_bp.route('/posts/<id>/', methods=['GET'])
def query_post_by_id(id):
    id = int(id)
    with open('utils/ghost/posts.json', 'r') as f:
        data = f.read()
    posts = json.loads(data).get('posts')
    for post in posts:
        if post.get('id') == id:
            resp = post
            break
    else:
        resp = {}
    return jsonify(**{'posts': [resp]})


@ghost_bp.route('/posts/<id>/', methods=['PUT'])
def update_post_by_id(id):
    id = int(id)
    new_post = json.loads(request.data)
    with open('utils/ghost/posts.json', 'r') as f:
        data = f.read()
    posts = json.loads(data).get('posts')
    for idx, post in enumerate(posts):
        if post.get('id') == id:
            posts[idx] = new_post

            break
    else:
        resp = {}
    return jsonify(**{'posts': [resp]})


@ghost_bp.route('/posts/slug/<slug>', methods=['GET'])
def query_post_by_slug(slug):
    pass


@ghost_bp.route('/tags/', methods=['GET'])
def query_tags():
    with open('utils/ghost/tags.json', 'r') as f:
        data = f.read()
    resp = json.loads(data)
    return jsonify(**resp)


@ghost_bp.route('/tags/<id>', methods=['GET'])
def query_tag_by_id(id):
    pass


@ghost_bp.route('/tags/slug/<slug>/', methods=['GET'])
def query_tag_by_slug(slug):
    pass


@ghost_bp.route('/slugs/post/<slug>/')
def query_slug_for_post(slug):
    return jsonify(**{"slugs": [{"slug": "untitled"}]})


@ghost_bp.route('/users/', methods=['GET'])
def query_users():
    with open('utils/ghost/users.json', 'r') as f:
        data = f.read()
    resp = json.loads(data)
    return jsonify(**resp)


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


@ghost_bp.route('/authentication/token', methods=['POST'])
def authentication_token():
    return jsonify(**{"access_token": "7Dvm9V6FkrKSiYfJa4aKsc8C0nzMzr7JmsSaM0U4z53qSpNPeSX4ljGjejsUNgxyEe2zwCsDUhRKnf92ITM5qDWfroVV3B6hNo3jobo0UbxFPGQjQgadUBhaNREBH1kgiXOjN2X5PJS12UFaVu4YQoJqOvjJEJVCVMdOyeQFqd59KCLL4GZJFFrcIIXztmd3DI9Wmt0zSnmuJaXMbI8sFCNf2UHOUhmmm1yF7mnf28hw72NTDCcaOUwGViO1ucs",
                      "refresh_token": "oNiRV8sTjXzFv2VtscHPzjGm3dRfYTmw5yhiIYDWi1FezNhEUZ5UT61Qu0pV6lKTXLdYyP1sCUdjXcwHVe94dzFWfKJ7O2VAOSlas233bGsES69zZ0l9Fo9ceA3KSOKZ8sKOPxKghQhHBSY9XYInZ6yMdOrIlQKA3Jc4T2YouGlAPwSROqTjvMMWBNDqohftgtyJ9EZ9jozc790lA5jPSnKwoc5taWt5g3dphQJx7rnjZxHyo4vxbnksSp47jNx",
                      "expires_in": 3600,
                      "token_type": "Bearer"})


@ghost_bp.route('/users/<user>/', methods=['GET'])
def query_user(user):
    with open('utils/ghost/users_{}.json'.format(user), 'r') as f:
        data = f.read()
    resp = json.loads(data)
    return jsonify(**resp)


@ghost_bp.route('/notifications/', methods=['GET'])
def notifications():
    return jsonify(**{"notifications": []})


