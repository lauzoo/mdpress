#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint


ghost_bp = Blueprint('ghost', __name__)


@ghost_bp.route('/posts', methods=['GET'])
def query_posts():
    pass


@ghost_bp.route('/posts/<id>', methods=['GET'])
def query_post_by_id(id):
    pass


@ghost_bp.route('/posts/slug/<slug>', methods=['GET'])
def query_post_by_slug(slug):
    pass


@ghost_bp.route('/tags', methods=['GET'])
def query_tags():
    pass


@ghost_bp.route('/tags/<id>', methods=['GET'])
def query_tag_by_id(id):
    pass


@ghost_bp.route('/tags/slug/<slug>', methods=['GET'])
def query_tag_by_slug(slug):
    pass


@ghost_bp.route('/users', methods=['GET'])
def query_users():
    pass


@ghost_bp.route('/users/<id>', methods=['GET'])
def query_user_by_id(id):
    pass


@ghost_bp.route('/users/slug/<slug>', methods=['GET'])
def query_user_by_slug(slug):
    pass


@ghost_bp.route('/users/email/<email>', methods=['GET'])
def query_user_by_email(email):
    pass
