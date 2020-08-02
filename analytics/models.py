import os
import math
import datetime
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils import timezone

class AnalyticQuerySet(models.query.QuerySet):

    def by_model(self, model_class, model_queryset=False):
        c_type = ContentType.objects.get_for_model(model_class)
        qs = self.filter(content_type=c_type)
        if model_queryset:
            viewed_ids = [x.object_id for x in qs]
            return model_class.objects.filter(pk__in=viewed_ids)
        return qs

    def search(self, query):
    	lookups = (Q(user__username__icontains=query) |
    	          Q(ip_address__icontains=query) |
    	          Q(content_object__icontains=query)
    	          )
    	return self.filter(lookups).distinct()

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
    	if number_of_weeks > weeks_ago:
    	    number_of_weeks = weeks_ago
    	days_ago_start = weeks_ago * 7  # days_ago_start = 49
    	days_ago_end = days_ago_start - (number_of_weeks * 7) #days_ago_end = 49 - 14 = 35
    	start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
    	end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
    	return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
    	if end_date is None:
    	    return self.filter(timestamp__gte=start_date)
    	return self.filter(timestamp__gte=start_date).filter(timestamp__gte=end_date)

    def by_date(self):
    	now = timezone.now() - datetime.timedelta(days=9)
    	return self.filter(timestamp__day__gte=now.day)

class AnalyticManager(models.Manager):
    def get_queryset(self):
        return AnalyticQuerySet(self.model, using=self._db)

    def by_model(self, model_class, model_queryset=False):
        return self.get_queryset().by_model(model_class, model_queryset=model_queryset)

    def get_by_id(self, id):
    	qs = self.get_queryset().filter(id=id)
    	if qs.count() == 1:
    	    return qs.first()
    	return None

    def search(self, query):
    	return self.get_queryset().search(query)

class Analytic(models.Model):
    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id           = models.PositiveIntegerField()
    content_object      = GenericForeignKey('content_type', 'object_id')
    timestamp           = models.DateTimeField(auto_now_add=True)
    view_count          = models.IntegerField(default=1)

    objects = AnalyticManager()

    def __str__(self):
        return "%s viewed on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-view_count']
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'

    @property
    def get_view_count(self):
        return self.view_count

