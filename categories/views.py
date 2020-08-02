from rest_framework import generics, permissions
from .serializers import CategorySerializer
from .models import Category
from faqs.models import Faq


class FaqCategoriesListAPIView(generics.ListAPIView): 
	permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
	serializer_class            = CategorySerializer
	queryset 					= Category.objects.all()

	def get_queryset(self, *args, **kwargs):
		queryset_list = []
		try:
			faq_qs = Faq.objects.all()
			queryset_list = Category.objects.filter(faq__in=faq_qs).distinct()
		except:
			pass
		return queryset_list

    