from django.conf.urls import url
from .views import FaqCategoriesListAPIView

app_name= 'categories'

urlpatterns = [
	 url(r'^faq/$', FaqCategoriesListAPIView.as_view(), name='list'),
]
