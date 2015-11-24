"""
Django settings for towpeb_H project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from braintree import Configuration, Environment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f-!cid_mmvn(8f+7wz6^vh#qwx3-zf303i-y)%kb3pkb9r(%be'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'America/Havana'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'Shop_Site'
)

SESSION_COOKIE_DOMAIN = '.hutton.es'

WEB_SITE_URL = 'http://www.hutton.es/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TPV_KEY = 'qwertyasdf0123456789'
TPV_FUC = '092508472'

# BRAINTREE_ENV = braintree.Environment.Sandbox
BRAINTREE_MERCHANT = 'rgrr3976xdtj9r9x'
BRAINTREE_PUBLIC_KEY = 'wp9wm59tpzg5ht43'
BRAINTREE_PRIVATE_KEY = '223d029cad5b5aa6dbcb93b3fba280a0'

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

# If you cannot install M2Crypto (e.g. AppEngine):
# BRAINTREE_UNSAFE_SSL = True

ROOT_URLCONF = 'towpeb_H.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'towpeb_H.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')  # change this to a proper location

EMAIL_HOST = 'smpt.hutton.es'

# EMAIL_HOST = 'mail.hutton.es'

EMAIL_HOST_USER = 'testing@hutton.es'

EMAIL_PORT = 578

# EMAIL_PORT = 587

EMAIL_USE_TLS = False

EMAIL_HOST_PASSWORD = '12345678a'

# THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.wand_engine.Engine'
