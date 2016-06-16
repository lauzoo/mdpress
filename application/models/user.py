#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db

from application.utils import format_datetime

__all__ = ['Permission', 'Role', 'User']


DEFAULT_AVATAR_URL = "https://www.gravatar.com/avatar/\
    3ca58cb0069eca6979b4a63cd6a5e478?s=64"


class Permission:
    READ = 0x01
    CREATE = 0x02
    UPDATE = 0x04
    DELETE = 0x08
    DEFAULT = READ
    ADMIN = READ | CREATE | UPDATE | DELETE


class Role(db.Model):
    uuid = db.Attribute(indexed=False)
    name = db.Attribute(required=True)
    description = db.Attribute(indexed=False)
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()
    permission = db.IntegerField(required=True)

    def __repr__(self):
        return "<{}-{:04X}>".format(self.name, self.permission)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

    def to_json(self, user):
        rst = self.attributes_dict
        rst["created_at"] = format_datetime(self.created_at)
        rst["updated_at"] = format_datetime(self.updated_at)
        rst["created_by"] = user.id
        rst["updated_by"] = user.id
        rst["id"] = self.id
        return rst


class User(db.Model):
    uuid = db.Attribute(indexed=False)
    name = db.Attribute(required=True)
    slug = db.Attribute(indexed=False)
    email = db.Attribute(required=True)
    avatar = db.Attribute(required=True, indexed=False,
                          default=DEFAULT_AVATAR_URL)
    password = db.Attribute(required=True, indexed=False)
    image = db.Attribute(indexed=False)
    cover = db.Attribute(indexed=False)
    bio = db.Attribute(indexed=False)
    website = db.Attribute(indexed=False)
    facebook = db.Attribute(indexed=False)
    twitter = db.Attribute(indexed=False)
    accessibility = db.BooleanField(indexed=False)
    status = db.Attribute()
    language = db.Attribute(indexed=False)
    visibility = db.BooleanField()
    meta_title = db.Attribute(indexed=False)
    meta_description = db.Attribute(indexed=False)
    tour = db.Attribute(indexed=False)
    last_login = db.DateTimeField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()
    role = db.ListField(Role, required=True)

    def to_json(self):
        rst = self.attributes_dict
        del rst['password']
        del rst['role']
        rst['id'] = self.id
        rst['last_login'] = format_datetime(self.last_login)
        rst['created_at'] = format_datetime(self.created_at)
        rst['updated_at'] = format_datetime(self.updated_at)
        rst['roles'] = [role.to_json(self) for role in self.role]
        return rst

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
