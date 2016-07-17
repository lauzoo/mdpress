#!/usr/bin/env python
# encoding: utf-8
import os
import wxr_parser

from application.models import Tag, Category, Post


def main():
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
        p = Post(title=post['title'], slug=post['slug'],
                 content=post['content'],
                 page=False, status=post['status'].upper(),
                 updated_at=post['pub_date']).save()
        print p

if __name__ == '__main__':
    main()
