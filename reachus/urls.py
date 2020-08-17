from django.conf.urls import url
from .views import ContactUsAPIView

app_name= 'reachus'

urlpatterns = [
	url(r'^$', ContactUsAPIView.as_view(), name='list'),
]
