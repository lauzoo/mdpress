#!/usr/bin/env python
# encoding: utf-8
import auth
import user
import post
import admin
import upload
import frontend

all_bp = [
    auth.auth_bp,
    user.user_bp,
    post.post_bp,
    admin.admin_bp,
    upload.upload_bp,
    frontend.frontend_bp,
]
