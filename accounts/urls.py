from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from .views import (
				AuthAPIView, 
				RegisterAPIView, 
				VerifyEmail, 
				RequestPasswordResetEmail,
				SetNewPasswordAPIView
				)


from rest_framework_simplejwt import views as jwt_views

app_name= 'accounts'

urlpatterns = [
    url(r'^email-verify/$', VerifyEmail.as_view(), name="email-verify"),
    url(r'^register/$', RegisterAPIView.as_view(), name='register'),
    path('jwt/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^request-reset-email/$', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    url(r'^password-reset-complete/$', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]