from django.conf.urls import url, include
from django.contrib import admin
from .views import AuthorPublicDetailAPIView

app_name= 'authors'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', AuthorPublicDetailAPIView.as_view(), name='author-detail'),
]

