# calculator/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    """
    Replaces a character with another in a string.
    Usage: {{ some_string|replace:"_, " }}
    """
    if len(arg.split(',')) != 2:
        return value
    
    what, to = arg.split(',')
    return value.replace(what, to)