from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LogoutView, PasswordResetConfirmView, PasswordResetView
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from apps.users import views

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
