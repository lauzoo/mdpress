#!/usr/bin/env python
# encoding: utf-8
from celery.util.log import get_task_logger

from app import celery


logger = get_task_logger(__name__)


@celery.task
def add(arg1, arg2):
    return arg1 + arg2
