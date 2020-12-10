from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Author
from .serializers import AuthorPublicSerializer

User = get_user_model()


# class AuthorPublicDetailAPIView(generics.RetrieveAPIView):
#     queryset            = Author.objects.filter(active=True)
#     serializer_class    = AuthorPublicSerializer


class AuthorPublicDetailAPIView(generics.GenericAPIView):
    serializer_class = AuthorPublicSerializer

    def get(self, request, username):

        try:
            user = User.objects.get(username=username)

            if user:
                author = Author.objects.get(user=user)
        except:
        	author = None
        return Response(AuthorPublicSerializer(author).data)
        # return AuthorPublicSerializer(author).data