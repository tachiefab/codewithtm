from django.contrib import admin
from .models import Like

class LikeAdmin(admin.ModelAdmin):
	
	list_display = [
				"__str__", 
				"content_object", 
				"content_type", 
				# "user",  
				"timestamp", 
				]
	search_fields = [
				"content_object", 
				]
	list_filter = [
				# "user", 
				"content_type",
				 ]

	class Meta:
		model = Like

admin.site.register(Like, LikeAdmin)
