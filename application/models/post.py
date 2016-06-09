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
    excerpt = db.Attribute(required=True)
    content = db.Attribute(indexed=False)
    user = db.ReferenceField(User, required=True)
    categories = db.ListField(Category)
    tags = db.ListField(Tag)
    create_at = db.DateTimeField(auto_now_add=True)
    version = db.IntegerField()
    last_update = db.DateTimeField(auto_now=True)
    comments = db.ListField(Comment)
    status = db.IntegerField(required=True)

    def to_json(self):
        cats = [Category.objects.filter(id=id).first().name for id in self.categories]
        tags = [Tag.objects.filter(id=id).first().name for id in self.tags]
        cmts = [Comment.objects.filter(id=id).first().to_json() for id in self.comments]
        return {
            "id": self.id,
            "title": self.title,
            "excerpt": self.excerpt,
            "content": self.content,
            "user": self.user.username,
            "categories": cats,
            "tags": tags,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "comments": cmts,
            "status": self.status
        }
