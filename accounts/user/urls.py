from django.conf.urls import url
from .views import UserDetailAPIView

app_name= 'accounts'

urlpatterns = [
    url(r'^(?P<username>\w+)/$', UserDetailAPIView.as_view(), name='detail'),
]

