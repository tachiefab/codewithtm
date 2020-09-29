from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .permissions import AnonPermissionOnly
from .serializers import (
                        UserRegisterSerializer, 
                        SetNewPasswordSerializer, 
                        ResetPasswordEmailRequestSerializer, 
                        EmailVerificationSerializer
                        )
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
                                smart_str, 
                                force_str, 
                                smart_bytes, 
                                DjangoUnicodeDecodeError
                                )
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse
from reachus.tasks import send_email

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class AuthAPIView(APIView):
    permission_classes      = [AnonPermissionOnly]
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(
                Q(username__iexact=username)|
                Q(email__iexact=username)
            ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({"detail": "Invalid credentials"}, status=401)


class RegisterAPIView(generics.GenericAPIView):

    serializer_class = UserRegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = settings.HOST_PRODUCTION_SERVER 
        absurl = current_site + "auth/very-email/" + str(token)

        username = user.username 
        preview_header = 'Please Use the link below to comfirm your email.'
        subject = 'Verify your email'
        message_first = """
                        you requested to creae an account with codewithtm with this email address.
                        If you did this, then please use the link below to comfirm your email address. 
                        """
        message_second= """
                        If you did not do this the please safely disregard this email.
                        """
        call2action_text = 'Confirm your email'
        call2action_link = absurl

        data = {
                'username':username, 
                'preview_header': preview_header,
                'subject': subject, 
                'message_first': message_first, 
                'message_second': message_second, 
                'call2action_text': call2action_text,
                'call2action_link': call2action_link,
                'to_email': user.email
                }

        send_email.delay(data)
        return Response(status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes          = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = settings.HOST_PRODUCTION_SERVER 
            absurl = current_site + "auth/password-reset/" + str(uidb64) + '/' + str(token)

            username = user.username 
            preview_header = 'Please use the link below to reset your password.'
            subject = 'Reset your passsword'
            message_first = """
                            you or someone pretending to be you requested to change your codewithtm password.\n
                            If you did this, then please use the link below to reset your password 
                            """
            message_second= """
                            If you did not do this the please safely disregard this email.
                            """
            call2action_text = 'reset password'
            call2action_link = absurl

            data = {
                    'username':username, 
                    'preview_header': preview_header,
                    'subject': subject, 
                    'message_first': message_first, 
                    'message_second': message_second, 
                    'call2action_text': call2action_text,
                    'call2action_link': call2action_link,
                    'to_email': user.email
                    }

            send_email.delay(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes          = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
