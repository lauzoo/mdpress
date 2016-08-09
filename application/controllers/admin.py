#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint, jsonify, render_template, request

import application.models as Models
from application.models.post import POST_STATUS
from application.utils import Pagination
from application.utils.response import normal_resp

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET'])
def index():
    all_posts = len(Models.Post.objects.all())
    published_posts = len(Models.Post.objects.filter(status=POST_STATUS[0]))
    draft_posts = len(Models.Post.objects.filter(status=POST_STATUS[1]))
    moderate_posts = len(Models.Post.objects.filter(status=POST_STATUS[2]))
    scheduling_posts = len(Models.Post.objects.filter(status=POST_STATUS[3]))
    return render_template('admin/index.html',
                           postnum={'total': all_posts, 'published': published_posts,
                                    'draft': draft_posts, 'moderate': moderate_posts,
                                    'scheduling': scheduling_posts})


@admin_bp.route('/login', methods=['GET'])
def login():
    return render_template('admin/login.html')


@admin_bp.route('/posts', methods=['GET'])
def all_posts():
    page = int(request.args.get('page', 1))
    posts = Models.Post.objects.all()
    page = Pagination(posts, page)
    return render_template('admin/post-list.html', page=page)


@admin_bp.route('/posts/oper', methods=['GET'])
def oper_post():
    id = request.args.get('pid')
    if id:
        post = Models.Post.objects.get_by_id(id)
        return render_template('admin/add-new.html', post=post)
    return render_template('admin/add-new.html')


@admin_bp.route('/tags', methods=['GET', 'POST'])
def all_tags():
    if request.method == 'GET':
        return render_template('admin/tag-list.html')
    else:
        tags = [tag.to_json() for tag in Models.Tag.objects.all()]
        rtn = {
            'page': 1,
            'total': len(Models.Tag.objects.all()),
            'rows': [{'id': tag.get('id'),
                      'cell': [tag.get('id'), tag.get('uuid'), tag.get('name'), tag.get('slug'), 0]} for tag in tags]
        }
        return jsonify(rtn)


@admin_bp.route('/categories', methods=['GET', 'POST'])
def all_categories():
    if request.method == 'GET':
        return render_template('admin/category-list.html')
    else:
        cates = [cate.to_json() for cate in Models.Category.objects.all()]
        rtn = {
            'page': 1,
            'total': len(Models.Category.objects.all()),
            'rows': [{'id': cate.get('id'),
                      'cell': [cate.get('id'), cate.get('uuid'), cate.get('name'), cate.get('slug'), 0]} for cate in cates]
        }
    return jsonify(rtn)


@admin_bp.route('/categories', methods=['PUT'])
def add_category():
    data = request.get_json()
    cate = Models.Category.objects.filter(name=data.get('category')).first()
    if not cate:
        cate = Models.Category.objects.create(name=data.get('category'))
        cate = Models.Category.objects.filter(name=data.get('category')).first()
    return normal_resp({'cate': cate.to_json()})


@admin_bp.route('/gallery', methods=['GET', 'POST'])
def all_gallery():
    if request.method == 'GET':
        return render_template('admin/upload-list.html')
    else:
        imgs = [img for img in Models.Images.objects.all()]
        rtn = {
            'page': 1,
            'total': len(Models.Images.objects.all()),
            'rows': [{'id': img.id,
                      'cell': img.to_json()} for img in imgs]
        }
    return jsonify(rtn)


@admin_bp.route('/comments', methods=['GET'])
def all_comments():
    return render_template('admin/comment-list.html')


@admin_bp.route('/settings', methods=['GET'])
def settings():
    return render_template('admin/profile.html')


@admin_bp.route('/other', methods=['GET'])
def other():
    pass
