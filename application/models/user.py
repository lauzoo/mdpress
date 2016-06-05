#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db

__all__ = ['Permission', 'Role', 'User']


class Permission:
    READ = 0x01
    CREATE = 0x02
    UPDATE = 0x04
    DELETE = 0x08
    DEFAULT = READ


class Role(db.Model):
    id = db.IntegerField(required=False)
    name = db.Attribute(required=True)
    permission = db.IntegerField(required=True)

    def __repr__(self):
        return "{}-{}".format(self.name, self.permission)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()


class User(db.Model):
    id = db.IntegerField(required=True)
    username = db.Attribute(required=True)
    password = db.Attribute(required=True, indexed=False)
    email = db.Attribute(required=True)
    role = db.IntegerField(required=True)

    def to_json(self):
        role = Role.objects.filter(id=self.role).first()
        return {"username": self.username,
                "email": self.email,
                "role": role.name}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
