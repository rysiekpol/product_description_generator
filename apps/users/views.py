# users/views.py

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.middleware import csrf
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers

User = get_user_model()


class UserRegisterationAPIView(RegisterView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer
    queryset = User.objects.all()

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     token = RefreshToken.for_user(user)
    #     data = serializer.data
    #     data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
    #     return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(LoginView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer
    queryset = User.objects.all()

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data
    #     serializer = serializers.CustomUserSerializer(user)
    #     token = RefreshToken.for_user(user)
    #     data = serializer.data
    #     data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
    #     return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(LogoutView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         refresh_token = request.data["refresh"]
    #         token = RefreshToken(refresh_token)
    #         token.blacklist()
    #         return Response(status=status.HTTP_205_RESET_CONTENT)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(UserDetailsView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user
