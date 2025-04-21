from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

extensions = ["pymdownx.arithmatex"]
extension_configs = {"pymdownx.arithmatex": {"generic": "True"}}


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(
        value, extensions=extensions, extension_configs=extension_configs
    )
