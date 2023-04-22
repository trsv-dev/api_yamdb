from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (User)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$'),
                    UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        read_only_fields = ['id']

    def create(self, value):
        return User.objects.create(**value)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Имя пользователя уже существует'
            )
        return value


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
