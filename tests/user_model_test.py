#!/usr/bin/env python
# encoding: utf-8
from unittest import TestCase

from application import create_app
import application.models as Models


class UserModelTest(TestCase):
    def setUp(self):
        self.app = create_app('TESTING')
        Models.Role.objects.create(
            id=10, name="Test",
            permission=Models.Permission.DELETE)

    def tearDown(self):
        for p in Models.User.objects.filter():
            p.delete()
        for p in Models.Role.objects.filter():
            p.delete()

    def test_save(self):
        r = Models.Role.objects.all()[0]
        u = Models.User(
            id=100000, username="zhangsan", password="zhangsan",
            email="zhangsan@test.com", role=r)
        self.assertTrue(u.is_valid(), msg=u.errors)
        status = u.save()
        self.assertTrue(status)
