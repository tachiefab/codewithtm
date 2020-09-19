from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from notifications.signals import notify
# from posts.models import Post

User = get_user_model()

# @task(name="notifications")
def do_notifications(username, target_id, content_type_id, verb):
  """
  Task to send a notification internally when a post is successfully created.
  """
  try:
    content_type = ContentType.objects.get_for_model(id=content_type_id)
    print(content_type)
    print("Hi Tachie You are Genuis")
    target = content_type.objects.get(id=target_id)
    print(target)
    user = get_object_or_404(User, username=username)
    user_qs = User.objects.filter(active=True)
    notification = notify.send( 
                            user,
                            action=target, 
                            target=target, 
                            receipient=user,
                            affected_users = user_qs,
                            verb= verb
                            )
    return notification
  except:
    return None



