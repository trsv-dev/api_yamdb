from django.core.validators import RegexValidator
from django.db.models import Q
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
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                "Имя пользователя 'me' зарезервировано в системе"
            )
        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')

        queryset = User.objects.filter(Q(username=username) | Q(email=email))

        for user in queryset:

            if username == user.username and email == user.email:
                return validated_data

            if user.username == username:
                raise serializers.ValidationError(
                    f'Пользователь с именем {username} уже существует!'
                )
            if user.email == email:
                print(user.email)
                raise serializers.ValidationError(
                    f'Пользователь с почтой {email} уже существует!'
                )
            if (user.username == username) or (user.email == email):
                raise serializers.ValidationError(
                    'Пользователь с такими данными уже существует!'
                )

        user = User.objects.create(**validated_data)
        return user


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
