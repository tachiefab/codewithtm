from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.serializers import ResetPasswordEmailRequestSerializer
from .models import MarketingPreference


class SubscribeToNewsLetter(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes          = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if email:
        	# user = None
        	MarketingPreference.objects.get_or_create(email=email)
        	message = 'Thanks for subscribing to our Newsletter.'
        return Response(message, status=status.HTTP_200_OK)
        

    