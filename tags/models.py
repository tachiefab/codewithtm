from django.db import models
from django.urls import reverse_lazy
from django.db.models.signals import pre_save
from codewithtm.utils import unique_slug_generator
from .signals import parsed_tags


class TagQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return super(TagManager, self).all(*args, **kwargs).active()


class Tag(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = TagManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp',]

def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(tag_pre_save_receiver, sender=Tag)

def parsed_tags_receiver(sender, tag_list, *args, **kwargs):
    if len(tag_list) > 0:
        for tag_var in tag_list:
            new_tag, create = Tag.objects.get_or_create(tag=tag_var)

parsed_tags.connect(parsed_tags_receiver)