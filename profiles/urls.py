from django.conf.urls import url
from .views import ProfileAPIDetailView, UpdateProfile 

app_name= 'profiles'

urlpatterns = [
    url(r'^(?P<pk>\d+)/profile/$', ProfileAPIDetailView.as_view(), name='profile'),
    url(r'^update/$', UpdateProfile.as_view(), name='profile_update'),
    # url(r'^(?P<pk>\d+)/update/$', UpdateProfile.as_view(), name='update'),
]