#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db

from .user import User


__all__ = ['Category', 'Tag', 'Post']


POST_STATUS = ('PUBLISHED', 'DELETED', 'EDITING', 'SCHEDULING')
COMMENT_STATUS = ('APPROVED', 'PENDING', 'DELETED')


class Category(db.Model):
    id = db.IntegerField(required=True)
    name = db.Attribute(required=True)
    super = db.IntegerField()


class Comment(db.Model):
    id = db.IntegerField(required=True)
    # 评论者的用户名
    author_name = db.Attribute()
    # 评论者的邮箱，如果没有设置头像会根据这个信息从gravatar获取头像
    author_email = db.Attribute()
    # 评论者的URL，评论者头像或者名字会跳转到改URL
    author_url = db.Attribute()
    # 评论者的IP
    ip = db.Attribute()
    # 评论者User Agent信息，通常包括浏览器版本、引擎、设备等信息
    agent = db.Attribute()
    # 这条评论被【赞】的次数，该属性导入意义不大，会在被喜欢之后重新统计
    likes = db.IntegerField()
    # 对这条评论点了【举报】的次数
    reports = db.IntegerField()
    # 评论发表时间。
    created_at = db.DateTimeField()
    # 评论状态。
    status = db.IntegerField()


class Tag(db.Model):
    id = db.IntegerField(required=True)
    name = db.Attribute()


class Post(db.Model):
    id = db.IntegerField(required=True)
    title = db.Attribute(required=True)
    slug = db.Attribute(required=True)
    markdown = db.Attribute(indexed=False)
    image = db.Attribute(indexed=False)
    featured = db.BooleanField()
    page = db.BooleanField()
    status = db.Attribute(required=True)
    language = db.Attribute(indexed=False)
    meta_title = db.Attribute(indexed=False)
    meta_description = db.Attribute(indexed=False)
    updated_at = db.DateTimeField(auto_now=True)
    updated_by = db.ReferenceField(User)
    published_at = db.DateTimeField()
    created_at = db.DateTimeField()
    created_by = db.ReferenceField(User)
    author = db.ReferenceField(User)
    publishedBy = db.ReferenceField(User)
    categories = db.ListField(Category)
    tags = db.ListField(Tag)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "markdown": self.markdown,
            "image": self.image,
            "featured": self.featured,
            "page": self.page,
            "status": self.status,
            "language": self.language,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.445Z"),
            "updated_by": self.updated_by.id if self.updated_by else None,
            "published_at": self.published_at.strftime("%Y-%m-%dT%H:%M:%S.445Z"),
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S.445Z"),
            "created_by": self.created_by.id if self.created_by else None,
            "author": "1",
            "publishedBy": self.publishedBy.id if self.publishedBy else None,
            "tags": []
        }
