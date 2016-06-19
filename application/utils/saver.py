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
            # print "save_model_from_json: {}".format(name)
            # print "save_model_from_json: {}".format(jobj.get(name))
            save_list_field(obj, field, jobj.get(name))
        if type(field) == db.Attribute:
            setattr(obj, name, jobj.get(name, None))
        if type(field) == db.DateTimeField:
            if jobj.get(name, None):
                field_val = parse(jobj.get(name))
                setattr(obj, name, field_val)

    # attr_dict = obj.attributes
    # for key, value in attr_dict.iteritems():
        # print "{}_{}".format(key, value._target_type)
        # setattr(obj, key, jobj.get(key, None))
    current_app.logger.info("save obj with errors: {}".format(obj.errors))
    obj.save()
    return not obj.errors, obj


def update_model_from_json(obj, jobj):
    attr_dict = obj.attributes
    current_app.logger.debug("update {} with {}".format(obj, jobj))
    for key, value in attr_dict.iteritems():
        print "{}_{}".format(key, value)
        if isinstance(value, db.DateTimeField) and jobj.get(key):
            d = datetime.strptime(jobj.get(key), "%Y-%m-%dT%H:%M:%S.%fZ")
            jobj[key] = d
        if jobj.get(key, None):
            setattr(obj, key, jobj.get(key))
    current_app.logger.debug("obj errors {}".format(obj.errors))
    obj.save()
    return not obj.errors, obj
