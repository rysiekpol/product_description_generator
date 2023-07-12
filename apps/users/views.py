# users/views.py

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import permissions, serializers

User = get_user_model()


class UserRegisterationAPIView(RegisterView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer
    queryset = User.objects.all()


class UserLoginAPIView(LoginView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer
    queryset = User.objects.all()


class UserLogoutAPIView(LogoutView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)


class UserAPIView(UserDetailsView):
    """
    Get, Update user information
    """

    def get_serializer_class(self):
        if self.request.user.is_super:
            return serializers.CustomUserAdminSerializer
        return serializers.CustomUserSerializer

    permission_classes = (IsAuthenticated,)
    serializer_class = get_serializer_class

    def get_object(self):
        return self.request.user


class CertainUserAPIView(UserDetailsView):
    """
    Get, Update certain user information
    """

    permission_classes = (IsAuthenticated, permissions.IsSuperUser)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(User, pk=pk)
