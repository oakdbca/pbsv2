"""Django Users Template Tag."""

# Third-Party
from django import template

from govapp import helpers

# Register Template Tag
register = template.Library()


@register.simple_tag(takes_context=True)
def is_internal(context):
    request = context["request"]
    return helpers.is_internal(request)


@register.simple_tag(takes_context=True)
def is_django_admin(context):
    request = context["request"]
    return helpers.is_django_admin(request.user)


@register.simple_tag(takes_context=True)
def is_pbs_admin(context):
    request = context["request"]
    return helpers.is_pbs_admin(request.user)
