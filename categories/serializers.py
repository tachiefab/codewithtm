from rest_framework import serializers
from .models import Category
from faqs.models import Faq
from faqs.serializers import FaqSerializer


class CategorySerializer(serializers.ModelSerializer):
	faqs         = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model= Category
		fields = [
			'title',
			'slug',
			'faqs',
		]

	def get_faqs(self, obj):
	    request = self.context.get('request')
	    limit = 10
	    if request:
	        limit_query = request.GET.get('posts_limit')
	        try:
	            limit = int(limit_query)
	        except:
	            pass
	    qs = Faq.objects.filter(category=obj)
	    data = FaqSerializer(qs[:limit], many=True, context={'request': request}).data
	    return data


class CategoryListSerializer(serializers.ModelSerializer):

	class Meta:
		model= Category
		fields = [
			'title',
			'slug',
		]
