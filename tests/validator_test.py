#!/usr/bin/env python
# encoding: utf-8
import logging
from unittest import TestCase

from voluptuous import Invalid

from application.utils.validator import user_schema, post_schema


class ValidateTest(TestCase):

    def setUp(self):
        pass

    def teaerDown(self):
        pass

    def test_normal_user_schema(self):
        try:
            user_schema({'username': 'zhangsan',
                         'password': 'password',
                         'email': 'zhangsan@test.com'})
        except Invalid as e:
            logging.error(e)
            self.assertTrue(False)

    def test_short_user_schema(self):
        try:
            user_schema({'username': 'z',
                         'password': 'password',
                         'email': 'zhangsan@test.com'})
            self.assertTrue(False)
        except Invalid as e:
            assert len(e.path) == 1
            assert e.path[0] == "username"

    def test_long_user_schema(self):
        try:
            user_schema({'username': 'zhangsanzhangsan1',
                         'password': 'password',
                         'email': 'zhangsan@test.com'})
            self.assertTrue(False)
        except Invalid as e:
            assert len(e.path) == 1
            assert e.path[0] == "username"

    def test_short_password_schema(self):
        try:
            user_schema({'username': 'zhangsan',
                         'password': 'passwor',
                         'email': 'zhangsan@test.com'})
            self.assertTrue(False)
        except Invalid as e:
            assert len(e.path) == 1
            assert e.path[0] == "password"

    def test_long_password_schema(self):
        try:
            user_schema({'username': 'zhangsan',
                         'password': 'passwordpassword1',
                         'email': 'zhangsan@test.com'})
            self.assertTrue(False)
        except Invalid as e:
            assert len(e.path) == 1
            assert e.path[0] == "password"

    def test_wrong_email_schema(self):
        try:
            user_schema({'username': 'zhangsan',
                         'password': 'password',
                         'email': 'zhangsantest.com'})
            self.assertTrue(False)
        except Invalid as e:
            assert len(e.path) == 1
            assert e.path[0] == "email"

    def test_long_email_schema(self):
        try:
            user_schema({'username': 'zhangsan',
                         'password': 'password',
                         'email': 'zhangsantestzhangsnatest@test.com'})
            self.assertTrue(False)
        except Invalid as e:
            assert len(e.path) == 1
            assert e.path[0] == "email"

    def test_normal_post(self):
        try:
            post_schema({
                'title': 'test',
                'excerpt': 'test-post',
                'content': 'content',
                'categories': ["1", "2"],
                'tags': ["hello", "world"],
                'status': 0
            })
        except Invalid as e:
            print e
            self.assertTrue(False)
