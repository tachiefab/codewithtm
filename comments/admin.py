from django.contrib import admin
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Comment


class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('timestamp',)
        widgets = {
            'content': CKEditorUploadingWidget(),
        }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = [
                    "user", 
                    "content_type", 
                    "content_object", 
                    "parent", 
                    "content", 
                    "name", 
                    "email", 
                    "website", 
                    "timestamp"
                    ]
	search_fields = ["user", "content"]
	list_filter = ["user", "content"]

	form = CommentAdminForm