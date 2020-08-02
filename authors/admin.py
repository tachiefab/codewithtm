from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Author


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('updated', 'timestamp')
        widgets = {
            'biography': CKEditorUploadingWidget(),
        }


@admin.register(Author)
class AuthorAdminForm(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp', 'updated', 'active']
    date_hierarchy = 'timestamp'
    list_filter = ('timestamp',)

    form = AuthorAdminForm
