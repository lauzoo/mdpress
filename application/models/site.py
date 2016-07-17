#!/usr/bin/env python
# encoding: utf-8
from redisco import models as db


class Site(db.Model):
    title = db.Attribute(indexed=False)   # 网站的标题
    site_path = db.Attribute(indexed=False)   # 字符全部小写，/site_folder_name/
    domains = db.ListField(str)  # 网站的域名（多个）， 数组型
    tags = db.ListField(str)  # 当前网站(public)日志的tags，数据类型为数组，tag_name+tag_count
    avatar = db.Attribute(indexed=False)  # 网站所有者的头像地址
    configs = db.Attribute(indexed=False)  # 网站的自定义属性
    content = db.Attribute(indexed=False)  # 网站的描述(HTML)
    raw_content = db.Attribute(indexed=False)  # 网站的描述(TXT)
    template_key = db.Attribute(indexed=False)  # 网站模板包的key值
    owner_template_key = db.Attribute(indexed=False)  # 网站自行打包的模板包的key值
    config_path = db.Attribute(indexed=False)  # 当前生效的网站配置文件，比如site.txt
    comment_script = db.Attribute(indexed=False)  # 网站目录下comment_js.txt(md/mk/markdown)的内容
