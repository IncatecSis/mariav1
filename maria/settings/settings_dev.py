# settings/settings_dev.py

from .settings_base import *

DEBUG = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
