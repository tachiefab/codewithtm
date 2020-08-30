from django.conf.urls import url
from django.urls import path
from .views import LikeAPIView

app_name= 'likes'

urlpatterns = [
	# path('<obj_id>/<type>/',
 #         LikeAPIView.as_view(), name='like'),
    # url(r'^$', LikeToggleAPIView.as_view(), name='like'),
    # url(r'^(?P<pk>\d+)/$', LikeToggleAPIView.as_view(), name='like'),
]
