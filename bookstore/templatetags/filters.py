from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe

register = template.Library()


@register.filter
@stringfilter
def highlight_search(text, search):
    highlighted = text.replace(search, '<span class="highlight">{}</span>'.format(search))
    return mark_safe(highlighted)