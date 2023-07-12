from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic import TemplateView

from apps.users import views

# app_name = "users"

urlpatterns = [
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
    path("login/", views.UserLoginAPIView.as_view(), name="login"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout"),
    path("register/", views.UserRegisterationAPIView.as_view(), name="register"),
    path("details/", views.UserAPIView.as_view(), name="user"),
    path("details/<int:pk>/", views.CertainUserAPIView.as_view(), name="certain_user"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("resend-email/", ResendEmailVerificationView.as_view(), name="resend_email"),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-email-verification-sent/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
]

if api_settings.USE_JWT:
    from dj_rest_auth.jwt_auth import get_refresh_view
    from rest_framework_simplejwt.views import TokenVerifyView

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
