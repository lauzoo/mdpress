#!/usr/bin/env python
# encoding: utf-8
from application import create_app, celery

app = create_app(None)
app.app_context().push()
