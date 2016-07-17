#!/usr/bin/env python
# encoding: utf-8
import os
import wxr_parser

from application.models import Tag, Category, Post, Site


def clear_all():
    for site in Site.objects.all():
        site.delete()
    for tag in Tag.objects.all():
        tag.delete()
    for cate in Category.objects.all():
        cate.delete()
    for post in Post.objects.all():
        post.delete()
    for site in Site.objects.all():
        site.delete()


def main():
    clear_all()
    # parse a file
    path = os.path.dirname(os.path.realpath(__file__))
    wp = wxr_parser.parse(os.path.join(path, 'wp.xml'))
    Site(title="Angiris Council", site_path='/',
         domains=['liuliqiang.info'], tags=['blog']).save()
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
             page=False, status=post['status'].upper(),
             updated_at=post['pub_date']).save()

if __name__ == '__main__':
    main()
