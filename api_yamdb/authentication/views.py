from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_yamdb.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.tokens import AccessToken

from . import serializers
from .models import User
from django.contrib.auth.tokens import default_token_generator, \
    PasswordResetTokenGenerator


class CustomSignUp(generics.CreateAPIView,PasswordResetTokenGenerator):
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data['email']
            user, _ = User.objects.get_or_create(email=email,
                                                 username=username)
            confirmation_code = default_token_generator.make_token(user)
            message = (f'Здравствуйте, {username}!'
                       f' Это ваш код подтверждения {confirmation_code}')
            send_mail(
                'Код подтверждения',
                message,
                EMAIL_HOST_USER,
                [email]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(generics.ListCreateAPIView):
    serializer_class = serializers.ConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            user = get_object_or_404(User, username=username)
            print(user)
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response({'token': str(token)},
                                status=status.HTTP_200_OK)
        else:
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)
