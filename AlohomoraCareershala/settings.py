"""
Django settings for AlohomoraCareershala project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib.messages import constants
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's8+03rl^1b1z&nyzy!0okoz-wwl)m^f4i(00cohqus$u&0vh(j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['alohomoracareershala.herokuapp.com', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    # project-related apps
    'users.apps.UsersConfig',
    'dashboard.apps.DashboardConfig',
    'questionnaire.apps.QuestionnaireConfig',
    'errors.apps.ErrorsConfig',
    'api.apps.ApiConfig',

    # third party
    'crispy_forms',
    'grappelli',
    'rest_framework',
    'taggit',
    'django_extensions',

    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'AlohomoraCareershala.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AlohomoraCareershala.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DB_URL = os.environ.get('DATABASE_URL')
DATABASES = {'default': dj_database_url.parse(DB_URL, conn_max_age=600)}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# older configs
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATIC_ROOT_FOLDER_NAME = 'assets'
STATIC_ROOT = os.path.join(BASE_DIR, f'{STATIC_ROOT_FOLDER_NAME}/')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

# Custom User
AUTH_USER_MODEL = 'users.CustomUser'

# Email backend
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
# For SMTP support: https://sendgrid.com/docs/for-developers/sending-email/django/
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Auth-related settings
LOGIN_URL = '/users/login/'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Grappelli Admin Site
GRAPPELLI_ADMIN_TITLE = 'Alohomora CareerShala Admin Site'

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Messages Framework
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-info',
    constants.INFO: 'alert-info',
    constants.SUCCESS: 'alert-success',
    constants.WARNING: 'alert-warning',
    constants.ERROR: 'alert-danger',
}

# Django-Taggit
TAGGIT_CASE_INSENSITIVE = False

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{asctime}] {levelname} module:[{module}] {message}',
            'style': '{',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'verbose': {
            'format': '{asctime} {levelname} location:[{pathname}:{lineno}] thread:[{threadName}] {message}',
            'style': '{',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'warning.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    },
}

# PRODUCTION
PRODUCTION_SERVER = False
if os.environ.get("ALOHOMORA_PRODUCTION_SERVER_URL") is not None:
    PRODUCTION_SERVER = True
    DEBUG = False
    PRODUCTION_SERVER_URL = os.environ.get("ALOHOMORA_PRODUCTION_SERVER_URL")
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
