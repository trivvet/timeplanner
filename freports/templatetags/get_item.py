from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)[0]

@register.filter
def get_item_list(list, key):
	try:
		return list[key]
	except:
		return None
