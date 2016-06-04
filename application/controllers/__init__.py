#!/usr/bin/env python
# encoding: utf-8
import auth
import user
import todo
import upload
import frontend

all_bp = [
    auth.auth_bp,
    user.user_bp,
    todo.todo_bp,
    upload.upload_bp,
    frontend.frontend_bp,
]
