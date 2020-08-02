from django.conf import settings
from django.db import models
from codewithtm.validators import validate_content


class Author(models.Model):
	user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	biography = models.TextField(validators=[validate_content])
	active = models.BooleanField(default=True)
	updated     = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.user.username)

	