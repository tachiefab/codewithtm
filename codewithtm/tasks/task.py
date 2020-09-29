from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from notifications.signals import notify
from posts.models import Post
from profiles.models import Profile
from django.shortcuts import get_object_or_404

User = get_user_model()


def do_notifications(target_id, verb):
    target = Post.objects.get(id=target_id)
    user = get_object_or_404(User, username='tachiefab')
    receipient = get_object_or_404(Profile, user=user)
    user_qs = Profile.objects.all()
    notification = notify.send( 
                            receipient,
                            action=target, 
                            target=target, 
                            receipient=receipient,
                            affected_users = user_qs,
                            verb= verb
                            )
    return notification



