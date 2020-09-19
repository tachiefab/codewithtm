from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from codewithtm.tasks.task import do_notifications


@task(name="notifications")
def notifications(username, target_id, content_type_id, verb):
	"""
	Task to do internal notification 
	when a post is created
	"""
	do_notifications(username, target_id, content_type_id, verb)






@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

