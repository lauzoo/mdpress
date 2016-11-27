#!/usr/bin/env python
# encoding: utf-8
from urlparse import urljoin

from flask import request, Blueprint
from werkzeug.contrib.atom import AtomFeed

from application.models import Post, POST_STATUS


feed_bp = Blueprint('feed', __name__)

def make_external(url):
    return urljoin(request.url_root, url)


@feed_bp.route('/rss')
def recent_feed():
    feed = AtomFeed('Angiris Council',
                    feed_url=request.url, url=request.url_root)
    articles = Post.objects.filter(status=POST_STATUS[0]).order('-published_at')[:15]
    for article in articles:
        feed.add(article.title, unicode(article.content),
                 content_type='html',
                 author=article.author.name,
                 url=make_external('post/{}'.format(article.slug)),
                 updated=article.updated_at,
                 published=article.published_at)
    return feed.get_response()

