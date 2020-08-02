from django.conf.urls import url
from .views import FaqListAPIView

app_name= 'faqs'

urlpatterns = [
	url(r'^$', FaqListAPIView.as_view(), name='list'),
]
