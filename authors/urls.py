from django.conf.urls import url, include
from django.contrib import admin
from .views import AuthorPublicDetailAPIView

app_name= 'authors'

urlpatterns = [
    # url(r'^(?P<pk>\d+)/$', AuthorPublicDetailAPIView.as_view(), name='author-detail'),

    url(r'^(?P<username>\w+)/$', AuthorPublicDetailAPIView.as_view(), name='author-detail'),
   

    # path('password-reset/<uidb64>/<token>/',
    #      PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
]

