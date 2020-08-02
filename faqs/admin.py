from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Faq


class FaqAdminForm(forms.ModelForm):
    class Meta:
        model = Faq
        exclude = ('updated', 'timestamp', 'slug',)
        widgets = {
        'question': CKEditorUploadingWidget(config_name='small'),
        'answer': CKEditorUploadingWidget(config_name='small')
        }


@admin.register(Faq)
class FaqAdminForm(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp', 'active']
    date_hierarchy = 'timestamp'
    list_filter = ('timestamp',)

    form = FaqAdminForm
