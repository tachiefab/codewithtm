import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.serializers import SerializerMethodField, ModelSerializer
from rest_framework.reverse import reverse as api_reverse
from profiles.serializers import PublicProfileSerializer

User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    profile = PublicProfileSerializer(read_only=True)
    uri             = SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'profile'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

   