from django.conf.urls import include, url
from .views import UserNotificationListAPIView, NotificationRead

app_name= 'notifications'

urlpatterns = [
			url(r'^$', UserNotificationListAPIView.as_view(), name='list'),
    		url(r'^(?P<pk>\d+)/$', NotificationRead.as_view(), name='notifications_read'),
	]



