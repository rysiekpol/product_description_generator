from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "created_at",
            "updated_at",
            "is_super",
        )
        read_only_fields = ("created_at", "updated_at", "id", "is_super")


class CustomUserAdminSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model for superuser permissions.
    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "created_at",
            "updated_at",
            "is_super",
        )
        read_only_fields = ("created_at", "updated_at", "id")


class UserRegisterationSerializer(RegisterSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    username = None
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    def save(self, request):
        return super().save(request)


class UserLoginSerializer(LoginSerializer):
    """
    Serializer class to authenticate users with email and password.
    """

    username = None

    def authenticate(self, **options):
        return authenticate(self.context["request"], **options)
