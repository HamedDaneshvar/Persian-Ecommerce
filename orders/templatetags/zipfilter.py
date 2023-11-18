from django import template

register = template.Library()


@register.filter(name='multifor')
def zip_lists(a, b):
    """
    Custom Django template filter that takes two lists or iterables 'a' and 'b'
    and zips them together.

    Usage:
    {% load zipfilter %}

    {% for item_a, item_b in list_a|multifor:list_b %}
        {{ item_a }} - {{ item_b }}
    {% endfor %}

    This filter is useful when you need to iterate over two lists or iterables
    simultaneously in a Django template.

    Parameters:
    - a: First list or iterable to be zipped.
    - b: Second list or iterable to be zipped.

    Returns:
    - A list of tuples, where each tuple contains one item from 'a' and one
      item from 'b'.

    Example:
    list_a = [1, 2, 3]
    list_b = ['a', 'b', 'c']

    {% for item_a, item_b in list_a|multifor:list_b %}
        {{ item_a }} - {{ item_b }}
    {% endfor %}

    Output:
    1 - a
    2 - b
    3 - c
    """
    return zip(a, b)
