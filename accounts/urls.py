from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import AuthAPIView, RegisterAPIView, VerifyEmail

app_name= 'accounts'

urlpatterns = [
    url(r'^$', AuthAPIView.as_view(), name='login'),
    url(r'^email-verify/$', VerifyEmail.as_view(), name="email-verify"),
    url(r'^register/$', RegisterAPIView.as_view(), name='register'),
    url(r'^jwt/$', obtain_jwt_token),
    url(r'^jwt/refresh/$', refresh_jwt_token),
]