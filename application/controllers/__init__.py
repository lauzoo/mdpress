#!/usr/bin/env python
# encoding: utf-8
from . import auth
from . import feed
from . import user
from . import post
from . import admin
from . import upload
from . import frontend
from . import callback

all_bp = [
    auth.auth_bp,
    user.user_bp,
    post.post_bp,
    feed.feed_bp,
    admin.admin_bp,
    upload.upload_bp,
    frontend.frontend_bp,
    callback.callback_bp,
]
