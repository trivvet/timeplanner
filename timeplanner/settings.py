"""
Django settings for timeplanner project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from .sensitive_data import DATABASES
from .env_settings import (
    SECRET_KEY, 
    DEBUG, 
    PORTAL_URL, 
    ALLOWED_HOSTS, 
    STATIC_ROOT,
    # ADMIN_EMAIL, 
    # EMAIL_HOST, 
    # EMAIL_PORT,
    # EMAIL_HOST_USER, 
    # EMAIL_HOST_PASSWORD,
    # EMAIL_USE_TLS, 
    # EMAIL_USE_SSL
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Application definition

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # EXTERNAL APPS
    'crispy_forms',
    # INTERNAL APPS
    'freports',
    'business_card',
    'finance',
    'login',
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'timeplanner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'timeplanner.context_processors.relative_path',
                'timeplanner.context_processors.today_tasks',
            ],
        },
    },
]

WSGI_APPLICATION = 'timeplanner.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/login'

# settings for Django Axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 5
AXES_BEHIND_REVERSE_PROXY = True
AXES_REVERSE_PROXY_HEADER = 'REMOTE_ADDR'
AXES_NUM_PROXIES = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Logging
LOG_FILE = os.path.join(BASE_DIR, 'timeplanner.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters' : {
        'verbose': {
             'format': 
                 '%(levelname)s %(asctime)s %(module)s : %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        }
    },   
    'filters': {
       'debug_mod': {
           '()': 'django.utils.log.RequireDebugTrue',
       },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': ['debug_mod'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        # }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
