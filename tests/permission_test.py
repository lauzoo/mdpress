#!/usr/bin/env python
# encoding: utf-8
import json
from unittest import TestCase

from application import create_app
import application.models as Models


class PermissionTest(TestCase):
    def setUp(self):
        self.app = create_app("TESTING")
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        Models.Role.objects.create(id=1, name="READER", permission=Models.Permission.READ)
        Models.Role.objects.create(id=2, name="CREATER", permission=Models.Permission.CREATE)
        Models.Role.objects.create(id=3, name="UPDATER", permission=Models.Permission.UPDATE | Models.Permission.CREATE)
        Models.Role.objects.create(id=4, name="DELETER", permission=Models.Permission.DELETE | Models.Permission.CREATE)
        Models.Role.objects.create(id=5, name="READER", permission=Models.Permission.DEFAULT)

    def tearDown(self):
        for p in Models.Role.objects.all():
            p.delete()
        for p in Models.User.objects.all():
            p.delete()

    def user_add_post(self):
        post = {
            'title': 'title',
            'slug': 'excerpt',
            'markdown': 'content',
            'categories': [],
            'tags': [],
            'status': 'PUBLISHED'
        }
        resp = self.client.post(
            '/posts/post', data=json.dumps(post),
            headers={'Authorization': 'Bearer {}'.format(self.token),
                     'Content-Type': 'application/json'})
        resp_json = json.loads(resp.data)
        return resp_json

    def _get_all_post(self):
        return json.loads(self.client.get('/posts/all').data)['data']['posts']

    def user_update_post(self):
        post = self._get_all_post()[0]
        print "all post {}".format(post)
        post['title'] = 'new_title'
        resp = self.client.put(
            '/posts/post', data=json.dumps(post),
            headers={'Authorization': 'Bearer {}'.format(self.token),
                     'Content-Type': 'application/json'})
        resp_json = json.loads(resp.data)
        return resp_json

    def user_delete_post(self):
        self.user_add_post()
        old_posts = self._get_all_post()
        post = old_posts[0]
        data = {'ids': [int(post.get('id'))]}
        print data
        resp = self.client.delete(
            '/posts/post', data=json.dumps(data),
            headers={'Authorization': 'Bearer {}'.format(self.token),
                     'Content-Type': 'application/json'})
        resp_json = json.loads(resp.data)
        return resp_json

    def create_permission_user_and_login(self, permission):
        role = Models.Role.objects.filter(permission=permission).first()
        Models.User.objects.create(
            name="zhangsan", password="password",
            email="zhangsan@test.com", role=[role])
        print "create_permission_user_and_login with all user: {}".format(Models.User.objects.all())
        user = {
            'username': 'zhangsan@test.com',
            'password': 'password',
        }
        resp = self.client.post('/authentication/token', data=json.dumps(user),
                                headers={'Content-Type': 'application/json'})
        login_resp = json.loads(resp.data)
        print login_resp
        self.token = login_resp.get('access_token')

    def test_add_post_permission(self):
        self.create_permission_user_and_login(Models.Permission.CREATE)
        resp_json = self.user_add_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2000)
        self.assertEqual(resp_data.get('post').get('title'), 'title')
        self.assertIn('success', resp_msg)
        resp_json = self.user_update_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2009)
        self.assertEquals(resp_data, {})
        self.assertIn('no permission', resp_msg)
        resp_json = self.user_delete_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2009)
        self.assertEquals(resp_data, {})
        self.assertIn('no permission', resp_msg)

    def test_update_post_permission(self):
        self.create_permission_user_and_login(Models.Permission.UPDATE | Models.Permission.CREATE)
        resp_json = self.user_add_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2000)
        self.assertEqual(resp_data.get('post').get('title'), 'title')
        self.assertIn('success', resp_msg)
        resp_json = self.user_update_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2000)
        self.assertEqual(resp_data.get('post').get('title'), 'new_title')
        self.assertIn('success', resp_msg)
        resp_json = self.user_delete_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2009)
        self.assertEquals(resp_data, {})
        self.assertIn('no permission', resp_msg)

    def test_delete_post_permission(self):
        self.create_permission_user_and_login(
            Models.Permission.DELETE | Models.Permission.CREATE)
        resp_json = self.user_add_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2000)
        self.assertEqual(resp_data.get('post').get('title'), 'title')
        self.assertIn('success', resp_msg)
        resp_json = self.user_update_post()
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2009)
        self.assertEqual(resp_data, {})
        self.assertIn('no permission', resp_msg)
        resp_json = self.user_delete_post()
        print "resp_json: {}".format(resp_json)
        resp_code = resp_json.get('code')
        resp_data = resp_json.get('data')
        resp_msg = resp_json.get('msg')
        self.assertEquals(resp_code, 2000)
        self.assertEqual(resp_data.get('posts')[0].get('title'), 'title')
        self.assertIn('success', resp_msg)
