import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse
from profiles.models import Profile

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta             = api_settings.JWT_REFRESH_EXPIRATION_DELTA
User = get_user_model()
HOST_SERVER = settings.HOST_SERVER


class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    uri = serializers.SerializerMethodField(read_only=True)
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_image',
            'uri'
        ]

    def get_username(self, obj):
        try:
            username = obj.username
        except:
           username = obj.user.username
        return username

    def get_first_name(self, obj):
        try:
            first_name = obj.first_name
        except:
           first_name = obj.user.first_name
        return first_name

    def get_last_name(self, obj):
        try:
            last_name = obj.last_name
        except:
           last_name = obj.user.last_name
        return last_name

    def get_profile_image(self, obj):
        profile_obj = get_object_or_404(Profile, user__username=self.get_username(obj))
        if profile_obj:
            try:
                img = profile_obj.get_profile_image_url()
            except:
                img = profile_obj.user.profile.get_profile_image_url()
            image = HOST_SERVER + str(img)
        else:
            image = None
        return image

    def get_uri(self, obj):
        request = self.context.get('request')
        try:
            user_pk = obj.pk
        except:
            user_pk = obj.user.pk
        return api_reverse("api-author:author-detail", kwargs={"pk": user_pk}, request=request)


class UserRegisterSerializer(serializers.ModelSerializer):
    password2           = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token               = serializers.SerializerMethodField(read_only=True)
    expires             = serializers.SerializerMethodField(read_only=True)
    message             = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message',

        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering. Please verify your email before continuing."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists")
        return value

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw  = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data): 
        user_obj = User(
                username=validated_data.get('username'), 
                email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False
        user_obj.save()
        return user_obj
