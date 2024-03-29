"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', "django-insecure-x4b^@jo()78k24arp(n)ga+*z9g*eac8de$d!72qpfs3@ggv6*")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)
DEBUG_MAIL = env.bool('DEBUG_MAIL', False)
DISABLE_PASSWORD_VALIDATION = env.bool('DISABLE_PASSWORD_VALIDATION', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', [])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', [])

CORS_ALLOW_ALL_ORIGINS = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "django_celery_beat",
    "corsheaders",

    "app_users",
    "app_edu",
    "app_payments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'JWT': {
            'description': 'Bearer <token>',
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    }
}

if DEBUG:
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=30)
    }

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates"
        ],
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

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": env.str("DB_NAME", "homework_7"),
        "USER": env.str("DB_USER", "postgres"),
        "PASSWORD": env.str("DB_PASSWORD", ""),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.int("DB_PORT", 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

if DEBUG and DISABLE_PASSWORD_VALIDATION:
    AUTH_PASSWORD_VALIDATORS = []
else:
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

LANGUAGE_CODE = env.str('LANGUAGE_CODE', 'en-us')

TIME_ZONE = env.str('TIME_ZONE', 'UTC')
CELERY_TIMEZONE = TIME_ZONE

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "app_users.User"

INACTIVE_USERS_INTERVAL = timedelta(days=env.int('INACTIVE_USERS_INTERVAL', 30))
INACTIVE_USERS_CHECK_INTERVAL = INACTIVE_USERS_INTERVAL / 2

STRIPE_API_KEY = env.str('STRIPE_API_KEY')
STRIPE_ENDPOINT_SECRET = env('STRIPE_ENDPOINT_SECRET')

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')

CELERY_BEAT_SCHEDULE = {
    'Stripe status poll': {
        'task': 'app_payments.tasks.stripe_poll_status',
        'schedule': timedelta(seconds=env.int('STRIPE_STATE_POLL_INTERVAL', 10)),
    },

    'Disable inactive users': {
        'task': 'app_users.tasks.disable_inactive_users_task',
        'schedule': INACTIVE_USERS_CHECK_INTERVAL,
        'relative': True,
    }
}

APPLICATION_SCHEME = env.str('APPLICATION_SCHEME', 'https')
APPLICATION_HOSTNAME = env.str('APPLICATION_HOSTNAME', 'localhost')
if APPLICATION_HOSTNAME:
    ALLOWED_HOSTS.append(APPLICATION_HOSTNAME)
    CORS_ALLOWED_ORIGINS.append(f'{APPLICATION_SCHEME}://{APPLICATION_HOSTNAME}')
    CSRF_TRUSTED_ORIGINS.append(f'{APPLICATION_SCHEME}://{APPLICATION_HOSTNAME}')


CELERY_TASK_RETRY_COUNT = env.int('CELERY_TASK_RETRY_COUNT', 2)

if DEBUG_MAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / 'tmp/email'
else:
    EMAIL_BACKEND = env.str('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
    EMAIL_FILE_PATH = env.str('EMAIL_FILE_PATH', None)
    EMAIL_HOST = env.str('EMAIL_HOST')
    EMAIL_PORT = env.int('EMAIL_PORT', 465)
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', False)
    EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', True)
    DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')
