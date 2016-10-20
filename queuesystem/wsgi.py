"""
WSGI config for queuesystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "queuesystem.settings")
#
# application = get_wsgi_application()

import os
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, '..', 'vendor'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "queuesystem.settings")

application = get_wsgi_application()
