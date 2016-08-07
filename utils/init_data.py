#!/usr/bin/env python
# encoding: utf-8
import os
from HTMLParser import HTMLParser

import html2text
import wxr_parser

from application.models import Tag, Category, Post
from application.utils.template import format_markdown


def clear_all():
    for tag in Tag.objects.all():
        tag.delete()
    for cate in Category.objects.all():
        cate.delete()
    for post in Post.objects.all():
        post.delete()


def convert_status(status):
    status_dict = {
        "PUBLISH": "PUBLISHED"
    }
    return status_dict.get(status, 'PUBLISHED')


def convert_content(content):
    h = html2text.HTML2Text()
    markdown = h.handle(content)
    html = format_markdown(markdown)
    return markdown, html


def main(location):
    clear_all()
    html_parser = HTMLParser()

    # parse a file
    if not location:
        path = os.path.dirname(os.path.realpath(__file__))
        wp = wxr_parser.parse(os.path.join(path, 'wp.xml'))
    else:
        wp = wxr_parser.parse(location)

    tags = wp['tags']
    for _, kv in tags.iteritems():
        Tag(name=kv['title'], slug=kv['slug']).save()
    cates = wp['categories']
    for _, kv in cates.iteritems():
        Category(name=kv['title']).save()
    posts = wp['posts']
    for post in posts:
        markdown, content = convert_content(post['content'])
        Post(title=html_parser.unescape(post['title']),
             slug=post['slug'], content=content,
             markdown=markdown, page=False,
             status=convert_status(post['status'].upper()),
             published_at=post['pub_date']).save()

if __name__ == '__main__':
    main()
