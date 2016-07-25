#!/usr/bin/env python
# encoding: utf-8
import application.models as Models


def create_roles():
    role = Models.Role.objects.filter(name="DELETER").first()
    if not role:
        Models.Role.objects.create(name="READER",
                                   permission=Models.Permission.READ)
        Models.Role.objects.create(
            name="CREATER",
            permission=Models.Permission.CREATE | Models.Permission.READ)
        Models.Role.objects.create(
            name="UPDATER",
            permission=(Models.Permission.UPDATE | Models.Permission.CREATE |
                        Models.Permission.READ))
        Models.Role.objects.create(
            name="DELETER",
            permission=(Models.Permission.DELETE | Models.Permission.UPDATE |
                        Models.Permission.CREATE | Models.Permission.READ))
        print "create roles finish..."
    else:
        print "no need to create role..."


def create_admin():
    users = Models.User.objects.filter(name='admin').first()
    if not users:
        role = Models.Role.objects.filter(name='DELETER').first()
        Models.User(name="admin", password="admin",
                    email="liqianglau@outlook.com", role=[role]).save()
        print "create admin finish..."
    else:
        print "user admin exists..."


def create_default_category():
    cate = Models.Category.objects.filter(name="Default").first()
    if not cate:
        cate = Models.Category.objects.create(name="Default")
        print "create category finish..."
    else:
        print "default category exists..."


def init_db():
    create_roles()
    create_admin()
    create_default_category()
