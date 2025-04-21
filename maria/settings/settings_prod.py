# settings/settings_prod.py

from .settings_base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
