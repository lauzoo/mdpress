#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

import redisco.models as db
from flask import current_app
from dateutil.parser import parse

NORMAL_FIELD = [basestring, str, unicode, int, float, bool]


def is_normal_field(field_type):
    return field_type in NORMAL_FIELD


def is_reference_field(field):
    return field._target_type == db.ReferenceField


def save_reference_field(obj, field, id):
    if id:
        value = field._target_type.objects.get_by_id(int(id))
        assert value is not None
        setattr(obj, field.name, value)


def save_list_field(obj, field, ids):
    # print ids
    if ids:
        # print "has ids"
        elem_type = field._target_type
        # print "is_normal_field: {}".format(is_normal_field(elem_type))
        if is_normal_field(elem_type):
            setattr(obj, field.name, ids)
        else:
            values = []
            for id in ids:
                # print '{}-{}'.format(field.name, id)
                value = field._target_type.objects.get_by_id(int(id))
                assert value is not None
                values.append(value)
            setattr(obj, field.name, values)


def save_model_from_json(model, jobj):
    obj = model()
    for field in obj.fields:
        name = field.name
        if type(field) == db.ReferenceField:
            save_reference_field(obj, field, jobj.get(name))
        if type(field) == db.ListField:
            save_list_field(obj, field, jobj.get(name))
        if type(field) == db.Attribute:
            setattr(obj, name, jobj.get(name, None))
        if type(field) == db.DateTimeField:
            if jobj.get(name, None):
                field_val = parse(jobj.get(name))
                setattr(obj, name, field_val)

    current_app.logger.info("save obj with errors: {}".format(obj.errors))
    obj.save()
    return not obj.errors, obj


def update_model_from_json(obj, jobj):
    current_app.logger.debug("update {} with {}".format(obj, jobj))
    for field in obj.fields:
        name = field.name
        if type(field) == db.ReferenceField:
            save_reference_field(obj, field, jobj.get(name))
        if type(field) == db.ListField:
            save_list_field(obj, field, jobj.get(name))
        if type(field) == db.Attribute:
            setattr(obj, name, jobj.get(name, None))
        if type(field) == db.DateTimeField:
            if jobj.get(name, None):
                field_val = parse(jobj.get(name))
                setattr(obj, name, field_val)
    current_app.logger.info("update obj with errors: {}".format(obj.errors))
    obj.save()
    return not obj.errors, obj
