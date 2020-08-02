from django.conf.urls import url
from .views import MostViewedPostListAPIView

app_name = 'analytics'

urlpatterns = [
    url(r'^most-viewed/$', MostViewedPostListAPIView.as_view(), name='most_viewed'),
    ]
