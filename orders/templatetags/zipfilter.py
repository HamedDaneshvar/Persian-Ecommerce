from django import template

register = template.Library()

@register.filter(name='multifor')
def zip_lists(a, b):
	return zip(a, b)