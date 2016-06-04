#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db


class Post(db.Model):
    user_id = db.Attribute()
    title = db.Attribute()
    create_at = db.DateTimeField(auto_now_add=True)
    content = db.Attribute(indexed=False)
