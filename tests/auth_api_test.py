#!/usr/bin/env python
# encoding: utf-8
import json
from unittest import TestCase

from application import create_app
import application.models as Models


class PostApiTest(TestCase):
    def setUp(self):
        self.app = create_app('TESTING')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        r = Models.Role.objects.create(
            name="Test",
            permission=Models.Permission.DELETE)
        print "create role with error: {}".format(r.errors)
        user = Models.User(
            name="zhangsan", password="password",
            email="liqianglau@outlook.com", role=[r])
        print "setup with user error: {}".format(user.errors)
        user.save()

    def tearDown(self):
        for user in Models.User.objects.all():
            user.delete()
        for role in Models.Role.objects.all():
            role.delete()
        self.ctx.pop()

    def test_login(self):
        user = {
            'username': 'liqianglau@outlook.com',
            'password': 'password',
        }
        resp = self.client.post('/authentication/token', data=json.dumps(user),
                                headers={'Content-Type': 'application/json'})
        login_resp = json.loads(resp.data)
        token = login_resp.get('access_token')
        self.assertIsNotNone(token)
