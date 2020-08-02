from django.conf.urls import url
from .views import TagListAPIView

app_name= 'tags'

urlpatterns = [
    url(r'^$', TagListAPIView.as_view(), name='list'),
]
