#!/usr/bin/env python
# encoding: utf-8
from .user import *
from .upload import *
from .post import *
from .system import *


def all():
    result = []
    models = []

    for m in models:
        result += m.__all__

    return result

__all__ = all()
