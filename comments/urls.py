from django.conf.urls import url
from .views import (
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    CommentLikeAPIView,
    )

app_name= 'comments'

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    url(r'^(?P<pk>\d+)/like/$', CommentLikeAPIView.as_view(), name='comment-like'),
    # url(r'^(?P<slug>[\w-]+)/like/$', CommentLikeToggleAPIView.as_view(), name='like-toggle'),
]
