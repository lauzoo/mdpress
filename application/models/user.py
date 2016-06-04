#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db

__all__ = ['Role', 'User']


class Permission:
    READ = 0x01
    CREATE = 0x02
    UPDATE = 0x04
    DELETE = 0x08
    DEFAULT = READ


class Role(db.Model):
    name = db.Attribute(required=True)
    permission = db.IntegerField(required=True)

    def __repr__(self):
        return "{}-{}".format(self.name, self.permission)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()


class User(db.Model):
    name = db.Attribute(required=True)
    password = db.Attribute(required=True, indexed=False)
    email = db.Attribute(required=True)
    role = db.IntegerField(required=True)

    @property
    def id(self):
        return str(self._id)

    def to_json(self):
        role = Role.objects(id=self.role).first()
        return {"name": self.name,
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
