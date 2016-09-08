"""
WSGI config for charts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/opt/django/lacnic-charts/charts')
sys.path.append('/Users/agustin/git/lacnic-charts/charts')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "charts.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'charts.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
