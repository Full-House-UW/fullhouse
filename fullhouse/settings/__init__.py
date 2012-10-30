# Django settings for fullhouse project.

from default import *

try:
    from local import *
except ImportError:
    raise Exception("settings/local.py config required and not found")

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window;
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
LOGIN_REDIRECT_URL = '/'

