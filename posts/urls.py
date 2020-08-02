from django.conf.urls import url
from .views import (
	LikeToggleAPIView,
    PostAPIView, 
    PostAPIDetailView,
    RelatedPostAPIView,
    )

app_name= 'Posts'

urlpatterns = [
    url(r'^$', PostAPIView.as_view(), name='list'),
    url(r'^related/$', RelatedPostAPIView.as_view(), name='related-posts'),
    url(r'^(?P<slug>[\w-]+)/$', PostAPIDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),
]
