"""
Django settings for codewithtm project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&53v=7vth_pjs=v-wbl_z%2a0z_b622io+w(#i54$d)#5r^=lv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
HOST_PRODUCTION_SERVER =  'http://127.0.0.1:4200/'
HOST_SERVER =  'http://127.0.0.1:8000'
CORS_ORIGIN_WHITELIST = (
     'http://localhost:4200',
     'http://127.0.0.1:4200',
     'http://localhost:4000',
     'http://127.0.0.1:4000',
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tachiefab311@gmail.com' 
EMAIL_HOST_PASSWORD = 'tachiefab4974'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Your Name <you@email.com>'

ADMINS = (
    ('Admin', EMAIL_HOST_USER),
)
MANAGERS = ADMINS


# Application definition

INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.flatpages',
         # third party apps
        # 'django_celery_beat',
        # 'django_celery_results',
        'ckeditor',
        'ckeditor_uploader',
        'corsheaders',
        'phonenumber_field',
        'rest_framework',
         'drf_yasg',
        # local 
        'aboutus',
        'accounts',
        'analytics',
        'authors',
        'categories',
        'comments',
        'reachus',
        'faqs',
        'likes',
        'marketing',
        'notifications',
        'posts',
        'profiles',
        'tags',
]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MAILCHIMP_API_KEY = "6bea8167b652cb4cdce560afc772d0da-us10"
MAILCHIMP_DATA_CENTER = "us10"
MAILCHIMP_EMAIL_LIST_ID = "6d1b0d0d3e"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codewithtm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'codewithtm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Accra'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static_in_pro", "our_static"),
#     #os.path.join(BASE_DIR, "static_in_env"),
#     #'/var/www/static/',
# )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static-server', 'media-root')
# # MEDIA_URL = '/media/'
# # MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")
PROTECTED_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static-server", "protected")
# Sites framework

SITE_ID = 1


# ck editor settings
from codewithtm.ckeditorconf.conf import *

# Django Restframework settings
from codewithtm.restconf.main import *

# Celery settings
# CELERY_BROKER_URL = 'redis://h:pf93dec0495e2404b3a1ca0cd012fda43c09edbaa581ca2d5237e92e280eabc40@ec2-3-212-177-190.compute-1.amazonaws.com:27299'
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL 
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Heroku settings
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False



# *******************************************
# My custom configurations
# *******************************************
# For base url, include "/" at the end
BASE_URL = HOST_SERVER

# For app labels section here
APP_LABEL_MYROOT = 'codewithtm'

# Common Site Information here
SITE_SHORT_NAME = APP_LABEL_MYROOT
SITE_FULL_NAME = APP_LABEL_MYROOT
SITE_YEAR_STARTED = "2020"
SITE_URL_HOME = HOST_SERVER
SITE_SLOGAN = SITE_FULL_NAME + " - create, share, entertain"
SITE_CONTACT_US = BASE_URL + 'contact'

# common Company information
COMPANY_ADDRESS = "codewithtm Inc, 3rd Floor, Cocoa Board, Sunyani, Ghana."
UNSUBSCRIBE_MESSAGE = "Don't like these emails?"
UNSUBSCRIBE_LINK = "http://i.imgur.com/CScmqnj.gif"

# Minimum characters for search
# MIN_CHARS_SEARCH = 3
# https://cdn-7music-upload.s3.amazonaws.com/static/assets/icon/favicon-32x32.png
# App Common Information
APP_EMAIL_FROM = EMAIL_HOST_USER
APP_EMAIL_BCC = EMAIL_HOST_USER
# APP_URL_TOP_LOGO = URL + 'static/assets/icon/favicon-32x32.png'
# APP_USER_AUTH_RE_ACCESS_LOGIN_PAGE = 'helloworld'
# APP_SITE_TEMPLATE_COLOR ='#000000'

# Default Avatar
# DEFAULT_AVATAR = APP_URL_TOP_LOGO #STATIC_URL + 'assets/images/avatar.png'

# # Enable the defaut site framework
SITE_ID = 1