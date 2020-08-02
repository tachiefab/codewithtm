from django.db import models
from django.urls import reverse_lazy
from django.db.models.signals import pre_save
from codewithtm.utils import unique_slug_generator


class CategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return super(CategoryManager, self).all(*args, **kwargs).active()


class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = CategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse("api-categories:detail", kwargs={"pk": self.pk})


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(category_pre_save_receiver, sender=Category)