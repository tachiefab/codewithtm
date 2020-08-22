from django import forms
from django.utils import timezone
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
                    'slug', 
                    'order', 
                    'read_time', 
                    # 'height_field', 
                    # 'width_field', 
                    'updated', 
                    'timestamp'
                    )
        widgets = {
            'article': CKEditorUploadingWidget(),
            # 'article': CKEditorUploadingWidget(config_name='codewithtm'),
            'summary': CKEditorUploadingWidget(config_name='small'),
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'read_time', 'timestamp', 'updated', 'published_date', 'author']
    date_hierarchy = 'timestamp'
    list_filter = ('timestamp', 'status')
    search_fields = ['title']

    form = PostAdminForm
    # prepopulated_fields = {'slug': ('title',)}
