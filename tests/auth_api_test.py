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
        Models.Role.objects.create(
            id=1, name="Test",
            permission=Models.Permission.DELETE)
        r = Models.Role.objects.all()[0]
        Models.User(id=10000, username="zhangsan",
                    password="password",
                    email="liqianglau@outlook.com",
                    role=r).save()

    def tearDown(self):
        Models.User.objects.filter(id=10000).first().delete()
        self.ctx.pop()

    def test_login(self):
        user = {
            'email': 'liqianglau@outlook.com',
            'password': 'password',
        }
        resp = self.client.post('/auth', data=json.dumps(user),
                                headers={'Content-Type': 'application/json'})
        login_resp = json.loads(resp.data)
        token = login_resp.get('access_token')
        self.assertIsNotNone(token)
