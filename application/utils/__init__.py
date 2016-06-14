#!/usr/bin/env python
# encoding: utf-8
from redisco import get_client
from redisco.models.key import Key


def format_datetime(d):
    if d:
        return d.strftime("%Y-%m-%dT%H:%M:%S.445Z"),
    else:
        return None


def get_slug_id():
    k = Key('slug')
    db = get_client()
    return db.incr(k['id'])
