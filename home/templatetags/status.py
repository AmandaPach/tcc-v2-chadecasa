from django import template

register = template.Library()

@register.inclusion_tag("tags/status.html")
def status(is_active):
    return {"active": bool(is_active)}