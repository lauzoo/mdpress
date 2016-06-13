#!/usr/bin/env python
# encoding: utf-8
import auth
import user
import post
import upload
import frontend
import ghost

all_bp = [
    auth.auth_bp,
    user.user_bp,
    post.post_bp,
    upload.upload_bp,
    frontend.frontend_bp,
    ghost.ghost_bp,
]
