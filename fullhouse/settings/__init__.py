# Django settings for fullhouse project.

from default import *

try:
    from local import *
except ImportError:
    raise Exception("settings/local.py config required and not found")
