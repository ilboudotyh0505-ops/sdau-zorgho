"""
WSGI config for sdau_zorgho project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdau_zorgho.settings')

application = get_wsgi_application()
