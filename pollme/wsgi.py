"""
WSGI config for pollme project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollme.settings')

application = get_wsgi_application()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


application = WhiteNoise(application, root=os.path.join(BASE_DIR,'/static'))