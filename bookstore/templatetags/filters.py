from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe
import re

register = template.Library()


@register.filter
@stringfilter
def highlight_search(text, search):
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    new_value = pattern.sub('<span class="highlight">\g<0></span>', text)
    return mark_safe(new_value)
