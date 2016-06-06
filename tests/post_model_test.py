#!/usr/bin/env python
# encoding: utf-8
from unittest import TestCase

from application import create_app
from application.models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.app = create_app('TESTING')

    def tearDown(self):
        for p in Post.objects.filter():
            p.delete()

    def test_save(self):
        p = Post(id=1, title="123", excerpt="test", content="cnt",
                 user=1, categories=[], tags=[], version=1,
                 comments=[], status=0)
        self.assertTrue(p.is_valid(), msg=p.errors)
        status = p.save()
        self.assertTrue(status)
