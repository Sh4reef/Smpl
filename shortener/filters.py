from django import template
from django.utils.safestring import mark_safe
from django.core.validators import URLValidator

register = template.Library()

@register.filter
def safe(value):
	urlvalidator = URLValidator()
	if 'http' not in value and 'https' not in url:
		new_value = 'http://' + value
	try:
		urlvalidator(new_value)
		value = new_value
	except:
		return None
    return mark_safe(value)

