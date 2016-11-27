#!/usr/bin/env python
# encoding: utf-8
import application.models as Models


def build_categories_tree():
    cate_count = len(Models.Category.objects.all())
    result = []
    while len(result) < cate_count:
        for cate in Models.Category.objects.all():
            if cate.super:
                if str(cate.super) in result:
                    index = result.index(str(cate.super))
                    result.insert(index + 1, cate.id)
            else:
                if cate.id not in result:
                    result.append(cate.id)
    return result
