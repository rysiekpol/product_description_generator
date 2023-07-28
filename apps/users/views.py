# users/views.py

from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import serializers

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


class UserAPIView(UserDetailsView):
    """
    Get, Update user information
    """

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.UserAdminSerializer
        return serializers.UserSerializer

    permission_classes = (IsAuthenticated,)
    serializer_class = get_serializer_class

    def get_object(self):
        return self.request.user


class CertainUserAPIView(UserDetailsView):
    """
    Get, Update certain user information
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = serializers.UserAdminSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(User, pk=pk)


class LogoutAPIView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if api_settings.SESSION_LOGIN:
            django_logout(request)

        response = Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK,
        )

        if api_settings.USE_JWT:
            # NOTE: this import occurs here rather than at the top level
            # because JWT support is optional, and if `USE_JWT` isn't
            # True we shouldn't need the dependency
            from dj_rest_auth.jwt_auth import unset_jwt_cookies
            from rest_framework_simplejwt.exceptions import TokenError
            from rest_framework_simplejwt.tokens import RefreshToken

            cookie_name = api_settings.JWT_AUTH_COOKIE

            unset_jwt_cookies(response)

            if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(
                        request.COOKIES[api_settings.JWT_AUTH_REFRESH_COOKIE]
                    )
                    token.blacklist()
                except KeyError:
                    response.data = {
                        "detail": _("Refresh token was not included in request data.")
                    }
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, "args"):
                        if (
                            "Token is blacklisted" in error.args
                            or "Token is invalid or expired" in error.args
                        ):
                            response.data = {"detail": _(error.args[0])}
                            response.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            response.data = {"detail": _("An error has occurred.")}
                            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        response.data = {"detail": _("An error has occurred.")}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            elif not cookie_name:
                message = _(
                    "Neither cookies or blacklist are enabled, so the token "
                    "has not been deleted server side. Please make sure the token is deleted client side.",
                )
                response.data = {"detail": message}
                response.status_code = status.HTTP_200_OK
        return response
