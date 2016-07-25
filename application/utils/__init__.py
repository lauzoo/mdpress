#!/usr/bin/env python
# encoding: utf-8
import os
import math
import struct
from datetime import datetime

from redisco import get_client
from redisco.models.key import Key
from flask import render_template as render


def format_datetime(d):
    if d:
        return d.strftime("%Y-%m-%dT%H:%M:%S.445Z"),
    else:
        return None


def format_now_datetime(d):
    if not d:
        d = datetime.now()

    return d.strftime("%Y-%m-%dT%H:%M:%S.445Z"),


def get_slug_id():
    k = Key('slug')
    db = get_client()
    return db.incr(k['id'])


def ceil(v):
    return int(math.ceil(v))


class Pagination(object):

    def __init__(self, objects, page=1, per_page=16):
        self.page = page
        self.per_page = per_page
        self.objects = objects
        try:
            self.total_count = objects.count()
        except AttributeError:
            self.total_count = len(objects)

    @property
    def slice(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        if start < 0:
            start = 0
        if end < 0:
            end = 0
        return self.objects[start:end]

    @property
    def pages(self):
        return ceil(self.total_count / float(self.per_page))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or num > self.pages - right_edge or\
                    (num > self.page - left_current - 1 and
                     num < self.page + right_current):
                if last + 1 != num:
                    raise StopIteration
                yield num
                last = num


def security_random(min, max):
    four_random_bytes = struct.unpack("<L", os.urandom(4))[0]
    return four_random_bytes % (max - min) + min
