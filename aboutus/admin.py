from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import AboutUs


class AboutUsAdminForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        exclude = ('updated', 'timestamp')
        widgets = {
            'about': CKEditorUploadingWidget(),
            'contact_information': CKEditorUploadingWidget(config_name='small'),
        }


@admin.register(AboutUs)
class AboutUsAdminForm(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp', 'updated', 'active']
    date_hierarchy = 'timestamp'
    list_filter = ('timestamp',)

    form = AboutUsAdminForm
