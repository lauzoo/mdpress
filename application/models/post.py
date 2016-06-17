#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db

from .user import User
from application.utils import format_datetime


__all__ = ['Category', 'Tag', 'Post']


POST_STATUS = ('PUBLISHED', 'DELETED', 'EDITING', 'SCHEDULING')
COMMENT_STATUS = ('APPROVED', 'PENDING', 'DELETED')


class Category(db.Model):
    name = db.Attribute(required=True)
    super = db.IntegerField()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Comment(db.Model):
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
    uuid = db.Attribute(indexed=False)
    name = db.Attribute(indexed=False)
    slug = db.Attribute(indexed=False)
    hidden = db.BooleanField()
    parent = db.Attribute(indexed=False)
    image = db.Attribute(indexed=False)
    meta_title = db.Attribute(indexed=False)
    meta_description = db.Attribute(indexed=False)
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

    def to_json(self):
        rst = self.attributes_dict
        rst["id"] = self.id
        rst["created_at"] = format_datetime(self.created_at)
        rst["updated_at"] = format_datetime(self.updated_at)
        rst["created_by"] = None
        rst["updated_by"] = None
        return rst


class Post(db.Model):
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
        rtn = self.attributes_dict
        rtn["updated_at"] = format_datetime(self.updated_at)
        rtn["updated_by"] = self.updated_by.id if self.updated_by else None
        rtn["published_at"] = format_datetime(self.published_at),
        rtn["created_at"] = format_datetime(self.created_at),
        rtn["created_by"] = self.created_by.id if self.created_by else None,
        rtn["publishedBy"] = self.publishedBy.id if self.publishedBy else None,
        return rtn
