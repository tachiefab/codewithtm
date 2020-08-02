from django.contrib import admin
from .models import Analytic

class AnalyticAdmin(admin.ModelAdmin):
	
	list_display = [
				"__str__", 
				"content_object", 
				"content_type", 
				"timestamp", 
				"view_count"
				]
	list_filter = [
				"content_type"
				 ]

	class Meta:
		model = Analytic

admin.site.register(Analytic, AnalyticAdmin)
