from django.shortcuts import render, Http404, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly
from profiles.models import Profile
from notifications.serializers import NotificationDisplaySerializer, NotificationReadSerializer
from .models import Notification


User = get_user_model()


class UserNotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationDisplaySerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        username = self.request.user.username
        if username:
            user = get_object_or_404(User, username=username)
            profile_user = get_object_or_404(Profile, user=user)
            queryset_list = profile_user.notifications.all()
        return queryset_list


class NotificationRead(APIView):
    serializer_class = NotificationReadSerializer


    def get(sself, request, pk, format=None):
        user = get_object_or_404(Profile, user=request.user)
        notification = get_object_or_404(Notification, id=pk)
        try:
            next = request.GET.get('next', None)
            if notification.receipient == user:
                notification.read = True
                notification.save()
                if next is not None:
                    return HttpResponseRedirect(next)
                else:
                    return redirect("api-notifications:list")
            else:
                raise Http404
        except:
            return redirect("api-notifications:list")
