import math
import datetime
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class LikeManager(models.Manager):

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