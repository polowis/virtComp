"""
WSGI config for virtComp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
if os.environ.get('GITHUB_WORKFLOW'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.local_settings')

application = get_wsgi_application()
