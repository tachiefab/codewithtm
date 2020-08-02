from django.db import models
from codewithtm.validators import validate_content

class AboutUs(models.Model):
    about = models.TextField(validators=[validate_content])
    contact_information = models.TextField(validators=[validate_content])
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'About Us created at ' + str(self.timestamp)

    class Meta:
    	ordering = ['-timestamp']
    	verbose_name = 'About Us'
    	verbose_name_plural = 'About Us'
