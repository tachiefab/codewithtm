from rest_framework import generics, permissions
from .serializers import FaqSerializer
from .models import Faq


class FaqListAPIView(generics.ListAPIView): 
    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = FaqSerializer
    queryset 					= Faq.objects.all()

    