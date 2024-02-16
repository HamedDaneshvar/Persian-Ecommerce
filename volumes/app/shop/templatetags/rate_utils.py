from django import template

register = template.Library()


@register.filter(name='minus')
def minus(a, b):
    return int(b) - int(a)
