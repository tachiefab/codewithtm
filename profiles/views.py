from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import PublicProfileSerializer, UpdateProfileSerializer
from notifications.serializers import NotificationDisplaySerializer

User = get_user_model()

class ProfileAPIDetailView(generics.RetrieveAPIView):

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class            = PublicProfileSerializer
    queryset                    = Profile.objects.all()


class UpdateProfile(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes          = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        website = request.data['website']
        phone = request.data['phone']
        country = request.data['country']
        try:
            username = request.user.username
            user = User.objects.get(username=username)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            try:
                profile_obj = Profile.objects.get(user=user)
                profile_obj.website = website
                profile_obj.phone = phone
                profile_obj.country = country
                profile_obj.save()
            except:
                pass
            message = 'Profile updated Successfully'
            return Response(message, status=status.HTTP_200_OK)
        except:
            message = 'Profile updated failed'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


