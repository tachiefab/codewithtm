from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from .utils import Mailchimp

class MarketingPreference(models.Model):
    # user  = models.ForeignKey(
    #         settings.AUTH_USER_MODEL,
    #         null=True, 
    #         blank=True,
    #         on_delete=models.CASCADE, 
    #         related_name='email_list'
    #         )
    email                       =models.EmailField()
    subscribed                  = models.BooleanField(default=True)
    mailchimp_subscribed        = models.NullBooleanField(blank=True)
    mailchimp_msg               = models.TextField(null=True, blank=True)
    timestamp                   = models.DateTimeField(auto_now_add=True)
    updated                     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = Mailchimp().add_email(instance.email)

post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)

def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            # subscribing user
            status_code, response_data = Mailchimp().add_email(instance.email)
        else:
            # unsubscribing user
            status_code, response_data = Mailchimp().add_email(instance.email)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)



def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    if created:
        email = instance.email
        MarketingPreference.objects.get_or_create(email=email)

post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)



