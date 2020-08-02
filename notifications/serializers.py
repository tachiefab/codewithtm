from rest_framework import serializers
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )
from notifications.models import Notification
from django.urls import reverse_lazy
from accounts.api.serializers import UserPublicSerializer


class NotificationDisplaySerializer(serializers.ModelSerializer):
    sender_object = UserPublicSerializer(read_only=True)
    link = SerializerMethodField()
    target = SerializerMethodField()
    received_date = SerializerMethodField()
    status = SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'sender_object',
            'verb',
            'target',
            'link',
            'received_date',
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

    def get_received_date(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_status(self, obj):
        status = obj.read
        if status == True:
            status = "Read"
        else:
            status = "Unread"
        return status