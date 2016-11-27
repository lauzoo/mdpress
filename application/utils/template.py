#!/usr/bin/env python
# encoding: utf-8
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

from flask import current_app, render_template

from application.models.system import site
from application.services.system import has


base_env = {
    'site': site,
    'has': has,
    'tags': {
        'join': lambda x: '',
    },
    'category': {
        'join': lambda x: '',
    },
    '_': lambda x: x,
    'i18n': lambda x, y, z: y,
    'mobile_meta': lambda: '',
    'get_resource': lambda x: '',
}


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang_desc):
        if not lang_desc:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lang_split = lang_desc.split(":")
        lang = lang_split[0]
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(
            linenos=True,
            style=current_app.config.get("HIGHLIGHT_STYLE", "default"))
        return highlight(code, lexer, formatter)


def render_theme_template(template, **kwargs):
    kwargs.update(base_env)
    return render_template(template, **kwargs)


def format_markdown(mdstr):
    render = HighlightRenderer()
    markdown = mistune.Markdown(renderer=render)
    return markdown(mdstr)
