from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    custom = context['request'].GET.copy()
    for key, value in kwargs.items():
        custom[key] = value
    return custom.urlencode()
