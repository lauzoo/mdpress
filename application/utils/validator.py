#!/usr/bin/env python
# encoding: utf-8
import re

from voluptuous import All, Invalid, Length, Schema, Required


def validate_email(email):
    """Validate email."""
    if not re.match(r"[^@]{5,16}@[^@]{2,10}\.[^@]{3,5}", email):
        raise Invalid("This email is invalid.")
    return email


user_schema = Schema({
    'email': validate_email,
    'username': All(basestring, Length(min=5, max=16)),
    'password': All(basestring, Length(min=8, max=16))
})

post_schema = Schema({
    'title': All(basestring, Length(max=100)),
    'slug': All(basestring, Length(max=100)),
    'markdown': basestring,
    'meta_description': basestring,
    'categories': list,
    'published_at': basestring,
    'tags': list,
    'status': basestring,
})

post_update_schema = Schema({
    'id': basestring,
    'title': All(basestring, Length(max=100)),
    'slug': All(basestring, Length(max=100)),
    'markdown': basestring,
    'meta_description': basestring,
    'categories': list,
    'published_at': basestring,
    'tags': list,
    'status': basestring,
})

system_setting_schema = Schema({
    Required("blog_name"): basestring,
    Required("blog_url"): basestring,
    "duoshuo": basestring,
    Required("owner"): basestring,
    "password": basestring,
    "password_again": basestring,
    Required("theme"): basestring,
    "post_per_page": int,
    "file_path": basestring,
    "need_toc": bool,
    "post_content_type": basestring,
    "post_url_format": basestring
})
