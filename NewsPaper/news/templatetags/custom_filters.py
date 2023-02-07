from django import template


register = template.Library()


@register.filter()
def censor(value, arg):
    return value.replace(arg, 'р******')