from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields= ['id',]


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)




