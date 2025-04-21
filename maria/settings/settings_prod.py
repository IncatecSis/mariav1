# settings/settings_prod.py

from .settings_base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'maria.urls'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
