#!/usr/bin/env python
# encoding: utf-8
import pickle

from flask import current_app

import application.models as Models
from application.services.user import create_user


DEFAULT_BACKUP_FILE = '/tmp/posts.bak'


def import_posts():
    backup_file = current_app.config.get('BACKUP_FILE', DEFAULT_BACKUP_FILE)
    with open(backup_file, "rb") as f:
        data = f.read()

    users = Models.User.objects.all()
    if not users:
        user = create_user()
    else:
        user = users[0]
    records = pickle.loads(data)
    for post in records['posts']:
        post.author = user
        post.save()
    for cate in records['categories']:
        cate.save()
    for tag in records['tags']:
        tag.save()
    for image in records['images']:
        image.save()
    return True

def export_posts():
    post_bak = {"posts": [], "categories": [], "tags": [], "images": []}
    for post in Models.Post.objects.all():
        post_bak["posts"].append(post)
    for cate in Models.Category.objects.all():
        post_bak["categories"].append(cate)
    for tag in Models.Tag.objects.all():
        post_bak["tags"].append(tag)
    for image in Models.Images.objects.all():
        post_bak["images"].append(image)
    with open("/tmp/posts.bak", "wb") as f:
        f.write(pickle.dumps(post_bak))
    return True
