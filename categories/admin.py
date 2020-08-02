from django import forms
from django.contrib import admin
from .models import Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
        	'title',
        	'slug',
        	'active'
        ]


@admin.register(Category)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ('title',)
    search_fields = ['title']

    form = CategoryAdminForm
