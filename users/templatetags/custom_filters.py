from django import template

register = template.Library()

@register.filter
def length_is(value, length):
    try:
        return len(value) == int(length)
    except Exception:
        return False
