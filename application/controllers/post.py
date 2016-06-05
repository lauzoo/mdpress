#!/usr/bin/env python
# encoding: utf-8
from flask import request, jsonify, current_app, Blueprint
from flask_jwt import jwt_required


post_bp = Blueprint('posts', __name__, url_prefix='/posts')


@post_bp.route('/post', methods=['GET'])
@jwt_required()
def qry_post():
    pass


@post_bp.route('/post', methods=['POST'])
@jwt_required()
def add_post():
    data = request.get_json()
    current_app.logger.info("add post: {}".format(data))
    return jsonify(**data)


@post_bp.route('/post', methods=['PUT'])
@jwt_required()
def udt_post():
    pass


@post_bp.route('/post', methods=['DELETE'])
@jwt_required()
def del_post():
    pass
