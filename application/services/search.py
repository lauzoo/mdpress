#!/usr/bin/env python
# encoding: utf-8
import re

from flask import current_app

import application.models as Models

class QueryLanguage(object):
    DEFAULT_CONDITION_SPLITER = '&'
    DEFAULT_CONDITION_KEY_VALUE_SPLITER = ':'
    DEFAULT_LIST_SPLITER = ','

    query_schema = {
        'default': 'content',
        'fields': {
            'tag': list,
            'cate': list,
            'content': basestring
        }
    }

    def __init__(self, schema=None):
        if schema:
            self.query_schema = schema

    def parser_query_condition(self, sc):
        query_conditions = []

        pattern = re.compile(r'[^\\]{}'.format(self.DEFAULT_CONDITION_SPLITER))
        rep_ptn = re.compile(r'\\{}'.format(self.DEFAULT_CONDITION_SPLITER))
        start = 0

        mc = pattern.search(sc, start)
        while mc:
            content = re.sub(rep_ptn, self.DEFAULT_CONDITION_SPLITER,
                             sc[start: mc.end() - 1])
            query_conditions.append(content)
            start = mc.end()
            mc = pattern.search(sc, start)
        query_conditions.append(re.sub(rep_ptn, self.DEFAULT_CONDITION_SPLITER,
                                       sc[start:]))

        return query_conditions

    def split_query_condition(self, condition):
        pattern = re.compile(r'[^\\]{}'.format(
                self.DEFAULT_CONDITION_KEY_VALUE_SPLITER))
        rep_ptn = re.compile(r'\\{}'.format(
                self.DEFAULT_CONDITION_KEY_VALUE_SPLITER))

        mc = pattern.search(condition)
        if mc:
            key = re.sub(rep_ptn, ':', condition[:mc.end() - 1])
            value = re.sub(rep_ptn, ':', condition[mc.end():])
        else:
            key = self.query_schema['default']
            value = re.sub(rep_ptn, ':', condition)
        return {key: value}

    def parse_list_field(self, list_content):
        result_lst = []

        pattern = re.compile(r'[^\\]{}'.format(self.DEFAULT_LIST_SPLITER))
        rep_ptn = re.compile(r'\\{}'.format(self.DEFAULT_LIST_SPLITER))
        start = 0

        mc = pattern.search(list_content, start)
        while mc:
            result_lst.append(
                re.sub(rep_ptn, ',', list_content[start: mc.end() - 1]))
            start = mc.end()
            mc = pattern.search(list_content, start)

        result_lst.append(re.sub(rep_ptn, ',', list_content[start:]))

        return result_lst

    def parse_query_string(self, content):
        conditions = {}
        qry_cnds = self.parser_query_condition(content)
        for qry_cnd in qry_cnds:
            cond = self.split_query_condition(qry_cnd)
            key = cond.keys()[0]
            value_type = self.query_schema['fields'][key]
            if value_type == list:
                value = self.parse_list_field(cond[key])
            else:
                value = cond[key]
            conditions.update({key: value})
        return conditions


def _cates_valid(cates):
    if len(cates) > 10:
        current_app.logger.info("category len to more")
        return False
    for cate in cates:
        if not Models.Category.objects.filter(name=cate).first():
            current_app.logger.error("can't not found category: {}".format(cate))
            return False
    return True


def _tag_valid(tags):
    if len(tags) > 10:
        return False
    for tag in tags:
        if not Models.Tag.objects.filter(name=tag).first():
            return False
    return True


def _post_in_cates_and_tags(cates, tags):
    posts = []
    if not cates and not tags:
        return Models.Post.objects.filter(status='PUBLISHED').all().order('-published_at')

    for post in Models.Post.objects.filter(status='PUBLISHED').all().order('-published_at'):
        if cates:
            for cate in post.categories:
                if cate.name in cates:
                    posts.append(post)
                    continue
        if tags:
            for tag in post.tags:
                if tag in tags:
                    post.append(post)
                    continue
    return posts


def _post_contain_content(posts, content):
    result = []
    for post in posts:
        if post.content.find(content) != -1:
            result.append(post)
        elif post.title.find(content) != -1:
            result.append(post)
    return result


def search(query_string):
    qry_srv = QueryLanguage()
    qrys = qry_srv.parse_query_string(query_string)
    print "query_conditions: {}".format(qrys)
    if not _cates_valid(qrys.get('cate', [])) or\
            not _tag_valid(qrys.get('tag', [])):
        print "cate or tag not valid"
        return []
    posts = _post_in_cates_and_tags(qrys.get('cate'), qrys.get('tag'))
    print "post cate and tag count: {}".format(len(posts))
    return _post_contain_content(posts, qrys.get('content'))
