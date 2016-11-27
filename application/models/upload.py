#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db

__all__ = ['Upload', 'Cloud', 'Images']


class Cloud(db.Model):
    name = db.IntegerField(required=True)
    upload_url = db.IntegerField(required=True)
    app_key = db.Attribute(required=False)
    app_secret = db.Attribute(required=False)
    extras = db.Attribute(indexed=False)


class Upload(db.Model):
    post = db.IntegerField(required=True)
    filename = db.Attribute(required=True)
    local_path = db.Attribute(required=True)
    cloud = db.IntegerField(required=True)
    url = db.Attribute(required=True)
    done_at = db.DateTimeField(auto_now_add=True)


class Images(db.Model):
    post_id = db.IntegerField(required=True)
    status = db.Attribute(required=True, default="active")
    image_name = db.Attribute(indexed=False)
    height = db.IntegerField(indexed=False)
    width = db.IntegerField(indexed=False)
    url = db.Attribute(indexed=False)
    delete_url = db.Attribute()
    local_path = db.Attribute(indexed=False)

    def to_json(self):
        return {
            "id": self.id, "post_id": self.post_id,
            "image_name": self.image_name,
            "url": self.url, "local_path": self.local_path
        }
