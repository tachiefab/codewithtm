from rest_framework import generics
from .models import Author
from .serializers import AuthorPublicSerializer


class AuthorPublicDetailAPIView(generics.RetrieveAPIView):
    queryset            = Author.objects.filter(active=True)
    serializer_class    = AuthorPublicSerializer
