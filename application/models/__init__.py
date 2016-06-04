#!/usr/bin/env python
# encoding: utf-8
from user import *
from upload import *
from post import *


def all():
    result = []
    models = []

    for m in models:
        result += m.__all__

    return result

__all__ = all()
