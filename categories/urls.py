from django.conf.urls import url
from .views import FaqCategoriesListAPIView

app_name= 'categories'

urlpatterns = [
	 url(r'^$', FaqCategoriesListAPIView.as_view(), name='list'),
]
