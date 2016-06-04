#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db


__all__ = ['Upload']


class Cloud(db.Model):
    id = db.IntegerField(required=True)
    name = db.IntegerField(required=True)
    upload_url = db.IntegerField(required=True)
    app_key = db.Attribute(required=False)
    app_secret = db.Attribute(required=False)
    extras = db.Attribute(indexed=False)


class Upload(db.Model):
    id = db.IntegerField(required=True)
    post = db.IntegerField(required=True)
    filename = db.Attribute(required=True)
    local_path = db.Attribute(required=True)
    cloud = db.IntegerField(required=True)
    url = db.Attribute(required=True)
    done_at = db.DateTimeField(auto_now_add=True)
