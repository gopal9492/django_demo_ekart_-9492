from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='sum')
def sum(values, attribute):
    total = 0
    for item in values:
        total += getattr(item, attribute)
    return total
