#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

import redisco.models as db
from flask import current_app


def save_model_from_json(model, jobj):
    obj = model()
    attr_dict = obj.attributes
    for key, _ in attr_dict.iteritems():
        setattr(obj, key, jobj.get(key, None))
    obj.save()
    return not obj.errors


def update_model_from_json(obj, jobj):
    attr_dict = obj.attributes
    current_app.logger.info("update {} with {}".format(obj, jobj))
    for key, value in attr_dict.iteritems():
        print "{}_{}".format(key, value)
        if isinstance(value, db.DateTimeField) and jobj.get(key):
            d = datetime.strptime(jobj.get(key), "%Y-%m-%dT%H:%M:%S.%fZ")
            jobj[key] = d
        if jobj.get(key, None):
            setattr(obj, key, jobj.get(key))
    current_app.logger.info("obj errors {}".format(obj.errors))
    obj.save()
    return not obj.errors
