from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def verbose_name(value):
    return value._meta.verbose_name


@register.filter
def admin_edit_url(obj):
    url = reverse(
        f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
        args=[obj.id],
    )
    return url
