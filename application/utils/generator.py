#!/usr/bin/env python
# encoding: utf-8
import random

import application.models as Models


def generator_user_id():
    user = None
    while not user:
        id = random.randint(100000, 99999999)
        user = Models.User.objects.filter(id=id).first()
        if not user:
            return id


def generator_post_id():
    post = None
    while not post:
        id = random.randint(100000, 99999999)
        post = Models.Post.objects.filter(id=id).first()
        if not post:
            return id
