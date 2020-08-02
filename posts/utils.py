import datetime
import math
import re
from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)
    return int(read_time_min)


def get_post_for_direction(instance, direction):
	''' get next post instance based on direction and current post instance'''
	category = instance.category
	''' post_set will be invalid if related_name was set for category on post Model '''
	post_qs = category.post_set.all()
	if direction == "next":
		new_qs = post_qs.filter(order__gt=instance.order)
	else:
		new_qs = post_qs.filter(order__lt=instance.order).reverse()
	next_post = None
	if len(new_qs) >= 1:
		try:
			next_post = new_qs[0]
		except IndexError:
			next_post = None
	return next_post


	