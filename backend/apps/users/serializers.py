from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize User model.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "created_at",
            "updated_at",
            "is_staff",
        )
        read_only_fields = ("created_at", "updated_at", "id", "is_staff")


class UserAdminSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize User model for superuser permissions.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "created_at",
            "updated_at",
            "is_staff",
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
