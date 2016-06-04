#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from application.extensions import db


__all__ = ['Upload']


class Upload(db.Document):
    filename = db.StringField()
    local_path = db.StringField()
    url = db.StringField()
    done_at = db.DateTimeField(datetime.now)
