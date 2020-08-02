from django.db import models
from django.db.models.signals import pre_save
from codewithtm.utils import unique_slug_generator
from codewithtm.validators import validate_content
from categories.models import Category

class FaqQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class FaqManager(models.Manager):
    def get_queryset(self):
        return FaqQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return super(FaqManager, self).all(*args, **kwargs).active()


class Faq(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=140, blank=True, unique=True)
    category = models.ForeignKey(
                            Category, 
                            # related_name='category_faqs', 
                            on_delete=models.CASCADE,
                            blank=True,
                            null=True
                            )
    question = models.TextField(validators=[validate_content])
    answer = models.TextField(validators=[validate_content])
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = FaqManager()

    def __str__(self):
        return self.title

def faq_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(faq_pre_save_receiver, sender=Faq)