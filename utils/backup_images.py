#!/usr/bin/env python
# encoding: utf-8
from BeautifulSoup import BeautifulSoup

from application.models import Post, Images


def backup():
    for post in Post.objects.all():
        bs = BeautifulSoup(post.content)
        images = bs.findAll('img')
        if images:
            for img in images:
                for attr in img[0].attrs:
                    if attr[0] == 'src':
                        url = attr[1]
                        Images(post_id=post.id, url=url).save()


if __name__ == '__main__':
    backup()
