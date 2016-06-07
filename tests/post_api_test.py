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
        Models.User(id=10000, username="zhangsan",
                    password="password",
                    email="liqianglau@outlook.com",
                    role=1).save()
        user = {
            'email': 'liqianglau@outlook.com',
            'password': 'password',
        }
        resp = self.client.post('/auth', data=json.dumps(user),
                                headers={'Content-Type': 'application/json'})
        login_resp = json.loads(resp.data)
        self.token = login_resp.get('access_token')

    def tearDown(self):
        self.ctx.pop()

    def test_add_post(self):
        post = {
            'title': 'title',
            'excerpt': 'excerpt',
            'content': 'content',
            'categories': [],
            'tags': [],
            'status': 1
        }
        resp = self.client.post(
            '/posts/post', data=json.dumps(post),
            headers={'Authorization': 'JWT {}'.format(self.token),
                     'Content-Type': 'application/json'})
        resp_code = json.loads(resp.data).get('code')
        self.assertEquals(resp_code, 2000)
