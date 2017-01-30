"""
Django settings for amadeus project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import dj_database_url

from django.conf.global_settings import DATETIME_INPUT_FORMATS, DATE_INPUT_FORMATS

db_from_ev = dj_database_url.config(conn_max_age=500)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$=8)c!5)iha85a&8q4+kv1pyg0yl7_xe_x^z=2cn_1d7r0hny4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'widget_tweaks',
    'rolepermissions',
    'oauth2_provider',
    'rest_framework',
    'django_bootstrap_breadcrumbs',
    's3direct',
    'django_summernote',
    'session_security',
    'django_cron',

    'amadeus',
    'users',
    'notifications',
    'log',
    'categories',
    'subjects',
    'students_group',
    'topics',
    'pendencies',
    'file_link',
    'webpage',
    'mailsender',
    'security',
    'themes',
    'links'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'users.middleware.SessionExpireMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'log.middleware.TimeSpentMiddleware',
    #libs-middleware

]

ROOT_URLCONF = 'amadeus.urls'

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
                'amadeus.context_processors.theme',
                'amadeus.context_processors.notifies',
            ],
        },
    },
]

WSGI_APPLICATION = 'amadeus.wsgi.application'

SESSION_SECURITY_WARN_AFTER = 1140
SESSION_SECURITY_EXPIRE_AFTER = 1200
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Database
# https://docs.djangopr/*oject.com/en/1.9/ref/settings/#databases

DATABASES = { 'default': db_from_ev,
            }



#superuser: admin pass: amadeus2358

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

#Static files heroku
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "amadeus/static")
]

CRON_CLASSES = [
    'notifications.cron.Notify'
]

#SECURITY
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')

#Allow all host headers
ALLOWED_HOSTS = ['*']

# Files
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads')
MEDIA_URL = '/uploads/'


# Users
LOGIN_REDIRECT_URL = 'app:index'
LOGIN_URL = 'core:home'
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
ROLEPERMISSIONS_MODULE = 'amadeus.roles'

LOGS_URL = 'logs/'
#https://github.com/squ1b3r/Djaneiro


# E-mail
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'admin@amadeus.com.br'

# Messages
from django.contrib.messages import constants as messages_constants
MESSAGE_TAGS = {
    messages_constants.DEBUG: 'debug',
    messages_constants.INFO: 'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR: 'danger',
}

#Send email for forgot Password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'test@gmail.com'
SERVER_EMAIL = 'test@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'amadeusteste@gmail.com'
EMAIL_HOST_PASSWORD = 'amadeusteste'
# SMTP CONFIG
# EMAIL_BACKEND = 'core.smtp.AmadeusEmailBackend'

#API CONFIG STARTS
#TELL the rest framework to use a different backend
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',),
     'PAGE_SIZE': 10, #pagination purposes
}

OAUTH2_PROVIDER = {
    'SCOPES':{'read':'Read scope', 'write': 'Write scope'}
}
#API CONFIG ENDS


#For date purposes
DATETIME_INPUT_FORMATS.append('%d/%m/%y')
DATE_INPUT_FORMATS.append('%d/%m/%y')
DATETIME_INPUT_FORMATS.append('%m/%d/%y')
DATE_INPUT_FORMATS.append('%m/%d/%y')

#s3direct

# AWS keys
AWS_SECRET_ACCESS_KEY = ''
AWS_ACCESS_KEY_ID = ''
AWS_STORAGE_BUCKET_NAME = ''

S3DIRECT_REGION = 'sa-east-1'

from uuid import uuid4

S3DIRECT_DESTINATIONS = {
    # Specify a non-default bucket for PDFs
    'material': (lambda original_filename: 'uploads/material/'+str(uuid4())+'.pdf', lambda u: True, ['application/pdf']),

}

# FILE UPLOAD
MAX_UPLOAD_SIZE = 10485760

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '100%',
    'height': '300',

    # Use proper language setting automatically (default)
    'lang': None,

    # Or, set editor language/locale forcely
    'lang_matches': {
        'pt': 'pt-BR',
        },

    # Customize toolbar buttons
        'toolbar': [
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                  'strikethrough', 'clear']],
        ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video', 'hr']],
        ['view', ['fullscreen', 'codeview']],
        ['help', ['help']],
    ],

    # Need authentication while uploading attachments.
    'attachment_require_authentication': True,

    # Set `upload_to` function for attachments.
    #'attachment_upload_to': my_custom_upload_to_func(),

    

}

try:
    from .local_settings import *
except ImportError:
    pass