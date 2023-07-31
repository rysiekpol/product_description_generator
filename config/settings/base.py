"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

import dj_database_url
from pydantic import Extra, PostgresDsn
from pydantic_settings import BaseSettings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class SettingsFromEnvironment(BaseSettings):
    """Defines environment variables with their types and optional defaults"""

    # PostgreSQL
    DATABASE_URL: PostgresDsn

    # Django
    SECRET_KEY: str
    DEBUG: bool = False
    ALLOWED_HOSTS: list
    EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST: str = "mailhog"
    EMAIL_PORT: int = 1025
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = ""
    USE_R2: bool = True
    STORAGES: dict = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    }
    AWS_STORAGE_BUCKET_NAME: str
    AWS_S3_ENDPOINT_URL: str
    AWS_S3_ACCESS_KEY_ID: str
    AWS_S3_SECRET_ACCESS_KEY: str
    AWS_S3_SIGNATURE_VERSION: str = "s3v4"

    CELERY_BROKER_URL: str

    IMMAGA_API_KEY: str
    IMMAGA_API_SECRET: str
    GPT_API_KEY: str

    class Config:
        """Defines configuration for pydantic environment loading"""

        env_file = str(BASE_DIR / "config/settings/.env.dev")
        case_sensitive = True
        extra = Extra.ignore


config = SettingsFromEnvironment()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
DEBUG = config.DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY
ALLOWED_HOSTS = config.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    "apps.users",
    "apps.products",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework_simplejwt.token_blacklist",
    "celery",
    "drf_yasg",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.config()}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
# Cloudflare R2

if config.USE_R2:
    STORAGES = config.STORAGES
    AWS_STORAGE_BUCKET_NAME = config.AWS_STORAGE_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = config.AWS_S3_ENDPOINT_URL
    AWS_S3_ACCESS_KEY_ID = config.AWS_S3_ACCESS_KEY_ID
    AWS_S3_SECRET_ACCESS_KEY = config.AWS_S3_SECRET_ACCESS_KEY
    AWS_S3_SIGNATURE_VERSION = config.AWS_S3_SIGNATURE_VERSION

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

MEDIA_PRODUCTS_ROOT = "products"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User model
AUTH_USER_MODEL = "users.User"

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 25,
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "access-token",
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
    "REGISTER_SERIALIZER": "apps.users.serializers.UserRegisterationSerializer",
    "USER_DETAILS_SERIALIZER": "apps.users.serializers.UserSerializer",
    "LOGIN_SERIALIZER": "apps.users.serializers.UserLoginSerializer",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=2),
}

# Allauth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_AUTHENTICATION_METHOD = "email"

AUTHENTICATION_METHOD = "email"

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of allauth
    "django.contrib.auth.backends.ModelBackend",
    # allauth specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_LOGOUT_ON_GET = False

# Email
EMAIL_BACKEND = config.EMAIL_BACKEND
EMAIL_HOST = config.EMAIL_HOST
EMAIL_PORT = config.EMAIL_PORT

# Celery
CELERY_BROKER_URL = config.CELERY_BROKER_URL

# Production settings
if DEBUG == False:
    SECURE_HSTS_SECONDS = 3600
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    EMAIL_HOST_USER = config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = config.DEFAULT_FROM_EMAIL
    # Cloudflare proxy settings
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Auto change domain name
MIGRATION_MODULES = {
    "sites": "config.fixtures.sites_migrations",
}

# External API keys
IMMAGA_API_KEY = config.IMMAGA_API_KEY
IMMAGA_API_SECRET = config.IMMAGA_API_SECRET
GPT_API_KEY = config.GPT_API_KEY
