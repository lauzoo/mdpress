#!/usr/bin/env python
# encoding: utf-8
import urllib
import dropbox
from dropbox.files import WriteMode
from BeautifulSoup import BeautifulSoup

from application.models import Post, Images


dbx = dropbox.Dropbox("YOUR_ACCESS_TOKEN")


def save(url):
    filename = url.split('/')[-1]
    path = r"/usr/local/upload/{}".format(filename)
    try:
        data = urllib.urlopen(url).read()
    except Exception:
        return ""
    with open(path, "wb") as f:
        f.write(data)
    return path


def backup():
    for post in Post.objects.all():
        bs = BeautifulSoup(post.content)
        images = bs.findAll('img')
        if images:
            for img in images:
                for attr in img.attrs:
                    if attr[0] == 'src':
                        url = attr[1]
                        Images(post_id=int(post.id), url=url).save()

    for img in Images.objects.all():
        path = save(img.url)
        if path:
            img.local_path = path
            img.save()
            with open(img.local_path, 'rb') as f:
                image_name = '/' + img.local_path.split('/')[-1]
                dbx.files_upload(f, image_name, mode=WriteMode('overwrite'))


if __name__ == '__main__':
    backup()
