"""
WSGI config for HelloDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os, sys
site_user_root_dir = '/home/b/belogugx/inverse-projects.store/public_html'
sys.path.insert(0, site_user_root_dir + '/inverse')
sys.path.insert(1, site_user_root_dir + '/venv/lib/python3.11/site-packages/')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inverse.settings')

application = get_wsgi_application()
