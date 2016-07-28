#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from redisco import models as db

from application.utils import format_now_datetime

from .user import User

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
        rst["created_at"] = format_now_datetime(self.created_at)
        rst["updated_at"] = format_now_datetime(self.updated_at)
        rst["created_by"] = None
        rst["updated_by"] = None
        return rst


class Post(db.Model):
    title = db.Attribute(required=True)
    slug = db.Attribute(required=True)
    markdown = db.Attribute(indexed=False)
    content = db.Attribute(indexed=False)
    image = db.Attribute(indexed=False)
    featured = db.BooleanField()
    page = db.BooleanField()
    status = db.Attribute(required=True)
    language = db.Attribute(indexed=False)
    meta_title = db.Attribute(indexed=False)
    meta_description = db.Attribute(indexed=False)
    updated_at = db.DateTimeField(auto_now=True)
    updated_by = db.ReferenceField(User)
    published_at = db.DateTimeField(auto_now_add=True)
    created_at = db.DateTimeField()
    created_by = db.ReferenceField(User)
    author = db.ReferenceField(User)
    publishedBy = db.ReferenceField(User)
    categories = db.ListField(Category)
    tags = db.ListField(Tag)

    # 相对于站点目录的路径，全小写
    path = db.Attribute(required=False, indexed=False)
    # 文档的完整路径, 全小写
    full_path = db.Attribute(required=False, indexed=False)
    # 文档的完整路径, 保留大小写
    raw_path = db.Attribute(required=False, indexed=False)
    # path的父目录路径
    parent_path = db.Attribute(required=False, indexed=False)
    # full_path的父目录路径
    parent_full_path = db.Attribute(required=False, indexed=False)
    # raw_path的父目录路径
    parent_raw_path = db.Attribute(required=False, indexed=False)
    # 文档类型，有folder/post/image/file四种
    type = db.Attribute(required=False, indexed=False)
    # 文档的时间，比如可作为文章的发表时间
    date = db.DateTimeField(auto_now=True)
    # 文档最后修改时间，评论文章也会导致m_date变动
    m_date = db.Attribute(required=False, indexed=False)
    # 文档的最后修改时间
    raw_date = db.Attribute(required=False, indexed=False)
    # 用户自定义的位置, 浮点数类型
    position = db.Attribute(required=False, indexed=False)
    # 文档的大小
    size = db.Attribute(required=False, indexed=False)
    # 内容类型，比如image/jpeg
    content_type = db.Attribute(required=False, indexed=False)
    visits = db.Attribute(required=False, indexed=False)
    # 在不改变文件路径的前提下，约等于访问IP数
    _visits = db.Attribute(required=False, indexed=False)
    # 文件后缀名，比如jpg txt
    ext = db.Attribute(required=False, indexed=False)
    # TableOfContens, HTML格式
    toc = db.Attribute(required=False, indexed=False)
    # 文章封面, 从内容中提取出来的第一张图片
    cover = db.Attribute(required=False, indexed=False)
    # 纯文本格式的正文，不包含metadata
    raw_content = db.Attribute(required=False, indexed=False)
    # 原始正文，包含metadata信息
    _content = db.Attribute(required=False, indexed=False)
    # post的扩展属性
    metadata = db.Attribute(required=False, indexed=False)
    # 自定义的url
    url_path = db.Attribute(required=False, indexed=False)
    # '/post/’+url_path 或 /+url_path，视情况而定
    url = db.Attribute(required=False, indexed=False)
    # 评论数
    comments_count = db.Attribute(required=False, indexed=False)
    # 恒等于1
    posts_count = db.Attribute(required=False, indexed=False)

    def to_json(self):
        rtn = self.attributes_dict
        rtn["id"] = self.id
        rtn["date"] = format_now_datetime(self.updated_at)
        rtn["updated_by"] = self.updated_by.id if self.updated_by else None
        rtn["published_at"] = format_now_datetime(self.published_at),
        rtn["created_at"] = format_now_datetime(self.created_at),
        rtn["created_by"] = self.created_by.id if self.created_by else None,
        rtn["publishedBy"] = self.publishedBy.id if self.publishedBy else None,
        rtn["categories"] = [cate.to_json() for cate in self.categories]
        rtn["tags"] = [tag.to_json() for tag in self.tags]
        return rtn
