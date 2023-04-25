from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.models import (User)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields = ['id', ]

    def validate(self, data):
        username = data['username']
        email = data['email']

        is_user_exists = User.objects.filter(username=username).exists()
        is_email_exists = User.objects.filter(email=email).exists()

        if is_user_exists and is_email_exists:
            return data
        if is_user_exists or is_email_exists:
            raise serializers.ValidationError(
                f'Пользователь с такими данными уже существует!'
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" зарезервировано в системе'
            )

        User.objects.create(username=username, email=email)

        return data


class ConfirmationSerializer(serializers.Serializer):
    """Сериализатор кода подтверждения."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с User."""

    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ['id', ]


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с эндпоинтом 'me'."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
