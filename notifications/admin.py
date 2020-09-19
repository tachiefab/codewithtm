from django.contrib import admin
from .models import Notification

# class NotificationAdmin(admin.ModelAdmin):
	
# 	list_display = [
# 				"__str__", 
# 				"sender_object", 
# 				"verb", 
# 				"action_content_type", 
# 				"action_object", 
# 				"target_object", 
# 				"receipient",
# 				"read",
# 				"timestamp"
# 				]
# 	search_fields = [
# 				"receipient", 
# 				"action_object",
# 				"target_object", 
# 				]
# 	list_filter = [
# 				"receipient", 
# 				"action_object",
# 				"target_object", 
# 				 ]

# 	class Meta:
# 		model = Notification

# admin.site.register(Notification, NotificationAdmin)
admin.site.register(Notification)
