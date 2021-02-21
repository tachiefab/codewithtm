import math
import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from posts.models import Post
from notifications.tasks import notifications
# from .tasks import auto_create_likes
from comments.models import Comment

User = get_user_model()




class LikeManager(models.Manager):

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(LikeManager, self).filter(content_type=content_type, object_id= obj_id)
        return qs

    def like_toggle(self, authenticated_user, sender, like_obj):
     
        if authenticated_user in like_obj.liked.all():
            is_liked = False
            like_obj.liked.remove(authenticated_user)
        else:
            is_liked = True
            like_obj.liked.add(authenticated_user)
        return is_liked

class Like(models.Model):
    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id           = models.PositiveIntegerField()
    content_object      = GenericForeignKey('content_type', 'object_id')
    timestamp           = models.DateTimeField(auto_now_add=True)
    liked      			= models.ManyToManyField(
    										settings.AUTH_USER_MODEL, 
    										blank=True, 
    										related_name='likes'
    										)

    objects = LikeManager()

    def __str__(self):
        return "%s liked on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Like'
        verbose_name_plural = 'Like'

    @property
    def likes_count(self):
        count = self.liked.all().count()
        return count


def post_like_receiver(sender, instance, created, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    if created:
        '''updating post order to have equal value as the it'''
        instance.order = instance.id
        instance.save()
        '''saving post like instance'''
        # content_type_id = ContentType.objects.get_for_model(sender).id
        # auto_create_likes.delay(instance.id, 'post')

        new_like_obj = Like.objects.create(
                    content_type=c_type,
                    object_id=instance.id
            )

    ''' Notifying users of a new post '''
    target_id = instance.id
    user = get_object_or_404(User, username='tachiefab')
    username = user.username
    verb = 'created a new post called '
    # Uncomment to use celery
    # notifications.delay(target_id, verb)

post_save.connect(post_like_receiver, sender=Post)


def comment_like_receiver(sender, instance, created, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    if created:
        new_like_obj = Like.objects.create(
                    content_type=c_type,
                    object_id=instance.id
            )

post_save.connect(comment_like_receiver, sender=Comment)