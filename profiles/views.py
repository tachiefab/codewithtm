from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import PublicProfileSerializer

User = get_user_model()

class ProfileAPIDetailView(
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, 
                    generics.RetrieveAPIView
                    ):

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class            = PublicProfileSerializer
    queryset                    = Profile.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
