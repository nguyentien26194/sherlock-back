from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh' token")


class SignUpSerializer(serializers.Serializer):
    shop_url = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)
