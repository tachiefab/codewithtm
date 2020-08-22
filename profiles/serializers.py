from rest_framework.serializers import SerializerMethodField, ModelSerializer
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse
from django.shortcuts import get_object_or_404
from .models import Profile
from accounts.serializers import UserPublicSerializer

HOST_SERVER = settings.HOST_SERVER

class PublicProfileSerializer(ModelSerializer):
    first_name = SerializerMethodField(read_only=True)
    last_name = SerializerMethodField(read_only=True)
    profile_image = SerializerMethodField()
    bio = SerializerMethodField()
    location = SerializerMethodField()
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "location",
        ]
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name


    def get_profile_image(self, obj):
        try:
            img = obj.get_profile_image_url()
            image = HOST_SERVER + img
        except:
           image = obj.get_profile_image_url()
        return image

    def get_bio(self, obj):
        return obj.bio

    def get_location(self, obj):
        return obj.location

