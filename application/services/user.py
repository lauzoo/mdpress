#!/usr/bin/env python
# encoding: utf-8
import application.models as Models


def create_user(username="admin", password="admin"):
    user = Models.User.objects.filter(name=username).first()
    if not user:
        role = Models.Role.objects.filter(name="READER").first()
        if not role:
            role = Models.Role.objects.create(
                name="READER", permission=Models.Permission.READ)
        user = Models.User.objects.create(
            name=username, email='{}@liuliqinag.info'.format(username),
            role=[role], password=password)
    return user
