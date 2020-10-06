from django.conf.urls import url
from .views import FaqCategoriesListAPIView, CategoriesListAPIView

app_name= 'categories'

urlpatterns = [
	 url(r'^$', CategoriesListAPIView.as_view(), name='list'),
	 url(r'^faq/$', FaqCategoriesListAPIView.as_view(), name='faq-category-list'),

]
