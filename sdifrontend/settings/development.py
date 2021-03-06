"""
Django settings for sdifrontend project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from sdifrontend.settings.production import *

TMP_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, 'tmp'))

DEBUG = TEMPLATE_DEBUG = True
#COMPRESS_ENABLED = True
#COMPRESS_OFFLINE = True

SECRET = '42'

# opt for the local postgresql if possible. otherwise, fall back to
# sqlite3.
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

INTERNAL_IPS = ('127.0.0.1',)

#if 'debug_toolbar' not in INSTALLED_APPS:
#    INSTALLED_APPS += ('debug_toolbar',)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# python_social
# https://python-social-auth.readthedocs.io/en/latest/
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GLOBUS_KEY = 'db786b4f-5a50-47f5-bd13-9ea7f7d0599a'
SOCIAL_AUTH_GLOBUS_SECRET = 'tjxCHVIBGYNFnTFnAdMaOW5VfgZCw7PsHOyvjnzftQc='
SOCIAL_AUTH_GLOBUS_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
}
