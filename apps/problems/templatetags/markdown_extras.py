from django import template
from django.template.defaultfilters import stringfilter

import bleach
from bleach_whitelist import markdown_tags, markdown_attrs

import markdown as md

register = template.Library()

extensions = ["pymdownx.arithmatex"]
extension_configs = {"pymdownx.arithmatex": {"generic": "True"}}


@register.filter()
@stringfilter
def markdown(value):
    dirty_html = md.markdown(
        value, extensions=extensions, extension_configs=extension_configs
    )
    clean_html = bleach.clean(dirty_html, markdown_tags, markdown_attrs)
    return clean_html


@register.filter()
@stringfilter
def unsafe_markdown(value):
    """
    Renders Inline HTML in markdown.
    Not to be used with user input. Only to be used for static data like markdown files.
    """
    dirty_html = md.markdown(
        value, extensions=extensions, extension_configs=extension_configs
    )
    return dirty_html
