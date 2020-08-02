from rest_framework import generics, permissions
from .serializers import AboutUsSerializer
from .models import AboutUs


class AboutUsAPIView(generics.RetrieveAPIView): 
    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = AboutUsSerializer
    queryset 					= AboutUs.objects.all()

    