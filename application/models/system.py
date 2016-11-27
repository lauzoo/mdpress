#!/usr/bin/env python
# encoding: utf-8
site = {
    'title': 'Angiris Council',
    'raw_content': {
        'escaped': lambda : '',
    },
    'configs': {
        'disqus': False,
        'duoshuo': 'liqianglau',
        'domain': 'liuliqiang.info',
        'domains': ['liuliqiang.info'],
        'keywords': {
            'escaped': lambda : '',
        },

        'posts_per_page': 10,
        'toc': False,               # True/False
        'post_content_type': 'plain',   # plain/markdown
        'post_paragraph_indent': False,  # True/False
        'mathjax': False,   # True/False
        'file_path': 'static',  # path for pic

        'comment': True,        # True/False
        'sync_by_3rd': False,   # True/False
        'sync_by_3rd_public': False,    # True/False
        'users': ['username@password'],     # users
        'score_degree': 0.5,    # 计数单位可以简单的理解为天，一般建议为0.5，这样可以让一天之内的最新&最热数据排在最前面。

        'post_url_format': 'normal',    # normal或no_prefix。 如果是normal, 那么调用post.url的时候，格式为/post/<url_path>; 如果是no_prefix，则为/<url_path>。
        'scripts_per_page': '',     # 一般的谷歌统计代码、第三方评论代码可以写入到这个字段。它会在渲染HTML页面的时候，将里面的内容插入到body>html>之前。
        'scripts_for_doc': '',  # 效果同scripts_per_page，但是仅仅在使用过add_doc_actions时生效。一般比如是文章的详细页。
        'template_priority': 'auto',    # auto/self/default
        'template_inherit': True,   # True, False
        'template_clone_allowed': False,    # True/False
        'autoreload': True,     # True/False
    }
}
