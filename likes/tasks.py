from django.contrib.contenttypes.models import ContentType
from celery.decorators import task
# from .models import Like


# @task(name="Auto Create Likes")
# def auto_create_likes(target_id, content_type):
# 	"""
# 	Task to do internal notification 
# 	when a post is created
# 	"""
# 	c_type = ContentType.objects.get(model=content_type)
# 	# ContentType.objects.get(model='bookmark').id
# 	new_like_obj = Like.objects.create(
# 	                content_type=c_type,
# 	                object_id=target_id
# 	        )
# 	return new_like_obj

