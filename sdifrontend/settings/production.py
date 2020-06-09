"""
Django settings for sdifrontend project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

PROJECT_APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(PROJECT_APP_ROOT))
PUBLIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'public'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'io4o1_(a2m_9%oe8hzmo_$y(h#+*^@j1x+lplp@zq20u75@=n_'

# SECURITY WARNING: don't run with debug turned on in production!
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_distill',
    'fontawesome_5',
    'sass_processor',
    'social_django',
    'sdifrontend.apps.mainpage',
    'sdifrontend.apps.landingpage',
    'sdifrontend.apps.news'
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

ROOT_URLCONF = 'sdifrontend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_APP_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'nav_sidebar': 'sdifrontend.apps.mainpage.sidebar',
                'tagcloud': 'sdifrontend.apps.landingpage.tagcloud'
            }
        },
    },
]

WSGI_APPLICATION = 'sdifrontend.wsgi.application'

# Logging
# https://docs.djangoproject.com/en/3.0/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'sdifrontend.apps':{
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARN'),
            'propagate': True,
        },
        'sdifrontend.apps.mainpage.views.user':{
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        }
    },
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if 'SDI_DATABASE_USER' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': os.environ['SDI_DATABASE_USER'],
            'PASSWORD': os.environ['SDI_DATABASE_PASSWORD'],
            'NAME': os.environ['SDI_DATABASE_NAME'],
            'HOST': os.environ['SDI_DATABASE_HOST'],
            'PORT': os.environ['SDI_DATABASE_PORT'] ,
        }
    }
else: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'sdifrontend-devel.db'),
        }
    }

SILENCED_SYSTEM_CHECKS = ['mysql.E001']

AUTHENTICATION_BACKENDS = [
    'social_core.backends.globus.GlobusOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
]

# python_social
# https://python-social-auth.readthedocs.io/en/latest/
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_GLOBUS_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
}

# deployment
if 'SOCIAL_AUTH_GLOBUS_KEY' in os.environ:
    SOCIAL_AUTH_GLOBUS_KEY = os.environ['SOCIAL_AUTH_GLOBUS_KEY']
else:
    SOCIAL_AUTH_GLOBUS_KEY = '02e6545e-bf68-4a7f-93e2-b4f39bfd7b35'

if 'SOCIAL_AUTH_GLOBUS_SECRET' in os.environ:
    SOCIAL_AUTH_GLOBUS_SECRET = os.environ['SOCIAL_AUTH_GLOBUS_SECRET']
else:
    SOCIAL_AUTH_GLOBUS_SECRET = '/CtafrN//yrZyTwXQnhw+L7T+MKSY3KxfKRGFPAoBvM='


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "mainpage/bootstrap")
#]

INTERNAL_IPS = ['127.0.0.1']

DISTILL_DIR = os.path.join(BASE_DIR, 'public')
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# fontawesome
# https://github.com/BenjjinF/django-fontawesome-5
FONTAWESOME_5_ICON_CLASS = 'semantic_ui'
