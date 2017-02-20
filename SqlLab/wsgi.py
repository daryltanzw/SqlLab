"""
WSGI config for SqlLab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('C:/Users/Daryl/Bitnami Django Stack projects/SqlLab')
os.environ.setdefault("PYTHON_EGG_CACHE", "C:/Users/Daryl/Bitnami Django Stack projects/SqlLab/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SqlLab.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
