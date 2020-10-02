from rest_framework import serializers
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )
from notifications.models import Notification
from django.urls import reverse_lazy
from django.utils.timesince import timesince
from accounts.serializers import UserPublicSerializer


class NotificationDisplaySerializer(serializers.ModelSerializer):
    sender_object = UserPublicSerializer(read_only=True)
    link = SerializerMethodField()
    target = SerializerMethodField()
    slug = SerializerMethodField()
    timesince = SerializerMethodField()
    status = SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'sender_object',
            'verb',
            'target',
            'slug',
            'link',
            'timesince',
            'status',
            
            ]

    def get_link(self, obj):
        return obj.get_link
    

    def get_target(self, obj):
        try:
            target = obj.target_object.title
        except:
            try:
                target = obj.target_object.content
            except:
                target = obj.target_object.username
        return target


    def get_slug(self, obj):
        try:
            slug = obj.target_object.slug
        except:
            try:
                slug = obj.target_object.id
            except:
                slug = obj.target_object.username
        return slug

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_status(self, obj):
        status = obj.read
        if status == True:
            status = "Read"
        else:
            status = "Unread"
        return status

class NotificationReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            'read',
            ]