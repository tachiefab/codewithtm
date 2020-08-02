from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from .signals import notify

class NotificationQuerySet(models.query.QuerySet):
	def get_user(self, receipient):
		return self.filter(receipient=receipient)

	def mark_targetless(self, receipient):
		qs = self.unread().get_user(receipient)
		qs_no_target = qs.filter(target_object_id=None)
		if qs_no_target:
			qs_no_target.update(read=True)

	def mark_all_read(self, receipient):
		qs = self.unread().get_user(receipient)
		qs.update(read=True)

	def mark_all_unread(self, receipient):
		qs = self.read().get_user(receipient)
		qs.update(read=False)

	def unread(self):
		return self.filter(read=False)

	def read(self):
		return self.filter(read=True)

	def recent(self):
		return self.unread()[:5]


class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def all_unread(self, user):
		return self.get_queryset().get_user(user).unread()

	def all_read(self, user):
		return self.get_queryset().get_user(user).read()

	def all_for_user(self, user):
		self.get_queryset().mark_targetless(user)
		return self.get_queryset().get_user(user)

	def get_recent_for_user(self, user, num):
		return self.get_queryset().get_user(user)[:num]


class Notification(models.Model):
	sender_content_type = models.ForeignKey(
										ContentType, 
										on_delete=models.CASCADE, 
										related_name='nofity_sender'
									)
	sender_object_id = models.PositiveIntegerField()
	sender_object = GenericForeignKey("sender_content_type", "sender_object_id")
	verb = models.CharField(max_length=255)
	action_content_type = models.ForeignKey(
										ContentType, 
										on_delete=models.CASCADE, 
										related_name='notify_action', 
										null=True, 
										blank=True
									)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_object = GenericForeignKey("action_content_type", "action_object_id")
	target_content_type = models.ForeignKey(
										ContentType, 
										on_delete=models.CASCADE, 
										related_name='notify_target', 
										null=True, 
										blank=True
									)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = GenericForeignKey("target_content_type", "target_object_id")
	receipient = models.ForeignKey(
								settings.AUTH_USER_MODEL, 
								on_delete=models.CASCADE, 
								related_name='notifications'
							)
	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = None
		context = {
			"sender": self.sender_object,
			"verb": self.verb,
			"action": self.action_object,
			"target": self.target_object,
			"verify_read": reverse("notifications:notifications_read", kwargs={"id": self.id}),
			"target_url": target_url,
		}
		if self.target_object:
			if self.action_object and target_url:
				return "%(sender)s %(verb)s %(action)s with a url of : %(verify_read)s?next=%(target_url)s" %context
			if self.action_object and not target_url:
				return "%(sender)s %(verb)s %(action)s" %context
			return "%(sender)s %(verb)s" %context
		return "%(sender)s %(verb)s" %context
	
	@property	
	def get_link(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = reverse("notifications:notifications_all")
		
		context = {
			"sender": self.sender_object,
			"verb": self.verb,
			"action": self.action_object,
			"target": self.target_object,
			"verify_read": reverse("notifications:notifications_read", kwargs={"id": self.id}),
			"target_url": target_url,
		}
		if self.target_object:
			return "%(verify_read)s?next=%(target_url)s" %context
		else:
			return "%(verify_read)s?next=%(target_url)s" %context


def new_notification(sender, **kwargs):
	kwargs.pop('signal', None)
	receipient = kwargs.pop("receipient")
	verb = kwargs.pop("verb")
	affected_users = kwargs.pop('affected_users', None)
	if affected_users is not None:
		for u in affected_users:
			if u == sender:
				pass
			else:
				new_note = Notification(
					receipient=u,
					verb = verb, # smart_text
					sender_content_type = ContentType.objects.get_for_model(sender),
					sender_object_id = sender.id,
					)
				for option in ("target", "action"):
					try:
						obj = kwargs[option]
						if obj is not None:
							setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
							setattr(new_note, "%s_object_id" %option, obj.id)
					except:
						pass
				new_note.save()
	else:
		new_note = Notification(
			receipient=receipient,
			verb = verb, 
			sender_content_type = ContentType.objects.get_for_model(sender),
			sender_object_id = sender.id,
			)
		for option in ("target", "action"):
			obj = kwargs.pop(option, None)
			if obj is not None:
				setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
				setattr(new_note, "%s_object_id" %option, obj.id)
		new_note.save()
notify.connect(new_notification)







