from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import ContactUsSerailizer
from .utils import Util

class ContactUsAPIView(generics.GenericAPIView):
	permission_classes      = [permissions.AllowAny]
	serializer_class = ContactUsSerailizer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			data = serializer.validated_data
			full_name = data.get('full_name')
			email = data.get('email')
			subject = data.get('subject')
			message = data.get('message')
			data = {
			 		'email_body': message, 
			 		'to_email': email,
			    	'email_subject': subject
			    }
			Util.send_email(data)
			return Response({"success": "Sent"})
		else:
			return Response({'success': "Failed"}, status=status.HTTP_400_BAD_REQUEST)