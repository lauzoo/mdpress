#!/usr/bin/env python
# encoding: utf-8
import auth
import feed
import user
import post
import admin
import upload
import frontend
import callback

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
