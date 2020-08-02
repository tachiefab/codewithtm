from django import forms
from django.contrib import admin
from .models import Tag


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
        	'title',
        	'slug',
        	'active'
        ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ('title',)
    search_fields = ['title']

    form = TagAdminForm
