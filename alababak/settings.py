"""
Django settings for alababak project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import django_heroku
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "alababak", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "alababak", "static")
MEDIA_DIR = os.path.join(BASE_DIR, "alababak", "media")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'udi2s+pa_3xphtm-9upkzn7c0omv*my_e-up_d$ph++-z)g3kv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'custom_user.apps.CustomUserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities_light',
    'djmoney',
    'account',
    'location',
    'inventory',
    'orders',
    'home',
    'mptt',
    'currencies',
    'rest_framework',

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

ROOT_URLCONF = 'alababak.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'currencies.context_processors.currencies',
            ],
        },
    },
]

WSGI_APPLICATION = 'alababak.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ar', 'Arabic'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = '/alababak/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    STATIC_DIR,
]

# Media files uploaded by user (images etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

AUTH_USER_MODEL = 'custom_user.User'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ar', 'en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['EG', 'UAE', 'SA']

# ident pixilation for displaying category tree
MPTT_ADMIN_LEVEL_INDENT = 20

# Activate Django-Heroku.
django_heroku.settings(locals())

# Currencies in money field
CURRENCIES = ('USD', 'EUR', 'EGP')
CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €'), ('EGP', 'EGP E£')]
OPENEXCHANGERATES_APP_ID = "c2b2efcb306e075d9c2f2d0b614119ea"
ALLOW_UNICODE_SLUGS = True