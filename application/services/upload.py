#!/usr/bin/env python
# encoding: utf-8
import json

import requests
from flask import current_app

from application.models.upload import Images


def _build_upload_response(url, delete_url, width, height, filename):
    return {
        "url": url, "del_url": delete_url, "filename": filename,
        "width": width, "height": height
    }

def _upload_to_smms(local_path):
    url = current_app.config.get('CLOUD_UPLOAD_CONFIG').get('url')
    files = {'smfile': open(local_path, 'rb')}
    resp = json.loads(requests.post(url, files=files).text)
    if resp.get('code') == 'success':
        current_app.logger.debug("smms upload resp: {}".format(resp))
        data = resp.get('data')
        return _build_upload_response(
            data.get('url'), data.get('delete'), data.get('width'),
            data.get('height'), data.get('filename'))
    else:
        current_app.logger.error("smms upload fail with resp: {}".format(resp))
        return {}

def upload_to_cloud(post_id, local_path):
    if current_app.config.get('CLOUD_UPLOAD_SITE') == 'smms':
        resp = _upload_to_smms(local_path)
    else:
        return None

    if resp:
        image = Images(
            post_id=post_id, image_name=resp.get('filename'),
            height=resp.get('height'), width=resp.get('width'),
            url=resp.get('url'), delete_url=resp.get('del_url'),
            local_path=local_path)
        image.save()
        return image
    else:
        return None
