#!/usr/bin/env python
# encoding: utf-8
from celery.utils.log import get_task_logger



logger = get_task_logger(__name__)
info, error = logger.info, logger.error


def log_request(request_path, req_data):
    if request_path[:6] == '/admin' or request_path[:5] == '/auth':
        sc.api_call(
            "chat.postMessage", channel="#general", username='sophie',
            text="ip: {}\nrequest: {}".format(req_data['ip'], request_path),
            icon_emoji=':robot_face:'
        )

