#!/usr/bin/env python
# encoding: utf-8
import os

import html2text
import wxr_parser

from application.models import Tag, Category, Post


def clear_all():
    for tag in Tag.objects.all():
        tag.delete()
    for cate in Category.objects.all():
        cate.delete()
    for post in Post.objects.all():
        post.delete()


def main():
    clear_all()
    # init markdown convert
    h = html2text.HTML2Text()

    # parse a file
    path = os.path.dirname(os.path.realpath(__file__))
    wp = wxr_parser.parse(os.path.join(path, 'wp.xml'))
    tags = wp['tags']
    for _, kv in tags.iteritems():
        Tag(name=kv['title'], slug=kv['slug']).save()
    cates = wp['categories']
    for _, kv in cates.iteritems():
        Category(name=kv['title']).save()
    posts = wp['posts']
    for post in posts:
        Post(title=post['title'], slug=post['slug'],
             content=post['content'],
             markdown=h.handle(post['content']),
             page=False, status=post['status'].upper(),
             published_at=post['pub_date']).save()

if __name__ == '__main__':
    main()
