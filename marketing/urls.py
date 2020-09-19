from django.conf.urls import url
from .views import SubscribeToNewsLetter

app_name= 'marketing'

urlpatterns = [
    url(r'^subscribe/$', SubscribeToNewsLetter.as_view(), name="email-verify"),
]