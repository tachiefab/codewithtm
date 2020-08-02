from django.conf import settings
from django.db import models
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
    location = models.CharField(max_length=220, null=True, blank=True)
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
            image = None
        return image

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=settings.AUTH_USER_MODEL)

