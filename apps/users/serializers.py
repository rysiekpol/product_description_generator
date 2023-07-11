from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(UserDetailsSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    # class Meta:
    #     model = CustomUser
    #     fields = (
    #         "id",
    #         "email",
    #         "created_at",
    #         "updated_at",
    #         "is_super",
    #     )


class UserRegisterationSerializer(RegisterSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    username = None
    password1 = serializers.CharField(
        write_only=True, min_length=4, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, min_length=4, style={"input_type": "password"}
    )

    # def create(self, validated_data):
    #     if validated_data["password"] != validated_data["repeat_password"]:
    #         raise serializers.ValidationError("Passwords must match.")
    #     if CustomUser.objects.filter(email=validated_data["email"]).exists():
    #         raise serializers.ValidationError("User with this email already exists.")

    #     return CustomUser.objects.create_user(**validated_data)

    def get_cleaned_data(self):
        return {
            "password": self.validated_data.get("password", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.save()
        adapter.save_user(request, user, self)
        return user


class UserLoginSerializer(LoginSerializer):
    """
    Serializer class to authenticate users with email and password.
    """

    username = None

    def authenticate(self, **options):
        return authenticate(self.context["request"], **options)

    # class Meta:
    #     model = CustomUser
    #     fields = ("email", "password")
    #     extra_kwargs = {
    #         "password": {
    #             "write_only": True,
    #             "style": {"input_type": "password"},
    #         }
    #     }
