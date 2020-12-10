from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save


def upload_profile_image(instance, filename):
    return "profile/{username}/{filename}".format(username=instance.user.username, filename=filename)

class Profile(models.Model):
    user        = models.OneToOneField(
                                    settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE, 
                                    related_name='profile'
                                    )
    profile_image       = models.ImageField(upload_to=upload_profile_image, null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    website = models.CharField(max_length=220, null=True, blank=True)
    country = models.CharField(max_length=220, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.user.username

    @property
    def owner(self):
        return self.user

    def get_profile_image_url(self):
        try:
            image = self.profile_image.url
        except:
            image = 'https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909__340.png'
        return image

    def get_notifications(self):
        return self.notifications.all()

    def get_notifications_count(self):
        notifications = self.notifications.filter(read=False)
        notifications_count = notifications.count()
        if notifications_count > 99:
            count = "99+"
        else:
            count = notifications_count
        return count

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=settings.AUTH_USER_MODEL)

