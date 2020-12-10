
from celery.decorators import task
from codewithtm.tasks.task import do_notifications


@task(name="notifications")
def notifications(target_id, verb):
	"""
	Task to do internal notification 
	when a post is created
	"""
	do_notifications(target_id, verb)

