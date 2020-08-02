from django.conf import settings
from rest_framework.serializers import SerializerMethodField, ModelSerializer
from rest_framework.reverse import reverse as api_reverse
from profiles.models import Profile
from .models import Author

HOST_SERVER = settings.HOST_SERVER

class AuthorPublicSerializer(ModelSerializer):
    first_name = SerializerMethodField(read_only=True)
    last_name = SerializerMethodField(read_only=True)
    profile_image = SerializerMethodField()
    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "biography",
        ]
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name


    def get_profile_image(self, obj):
        try:
            img = obj.user.profile.get_profile_image_url()
            image = HOST_SERVER + img
        except:
           image = None
        return image
