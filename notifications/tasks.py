from celery.decorators import task
from codewithtm.tasks.task import do_notifications


@task(name="notifications")
def notifications(username, target_id, verb):
	"""
	Task to send a notification internally when a album is successfully created.
	"""
	do_notifications(username, target_id, verb)






