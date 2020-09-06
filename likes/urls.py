from django.conf.urls import url
from django.urls import path
from .views import LikedItemsListAPIView

app_name= 'likes'

urlpatterns = [
	url(r'^$', LikedItemsListAPIView.as_view(), name='list'),
]
