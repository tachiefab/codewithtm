from django.conf.urls import url
from .views import AboutUsAPIView

app_name= 'aboutus'

urlpatterns = [
     url(r'^(?P<pk>\d+)/$', AboutUsAPIView.as_view(), name='detail'),
]
