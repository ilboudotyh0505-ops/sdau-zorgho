"""
ASGI config for sdau_zorgho project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdau_zorgho.settings')

application = get_asgi_application()
