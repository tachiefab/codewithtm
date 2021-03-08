from django.conf.urls import url
from .views import FaqCategoriesListAPIView, CategoriesListAPIView

app_name= 'categories'

urlpatterns = [
<<<<<<< HEAD
	 url(r'^faq/$', FaqCategoriesListAPIView.as_view(), name='list'),
=======
	 url(r'^$', CategoriesListAPIView.as_view(), name='list'),
	 url(r'^faq/$', FaqCategoriesListAPIView.as_view(), name='faq-category-list'),

>>>>>>> 03e3eb9a21b6e78d4af344e521f34037556ee78d
]
