from rest_framework import serializers
from .models import AboutUs
from categories.serializers import CategorySerializer


class AboutUsSerializer(serializers.ModelSerializer):
	class Meta:
		model= AboutUs
		fields = [
			'about',
			'contact_information',
		]

