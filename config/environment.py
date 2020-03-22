import os

DJANGO_ENV = os.environ.get('DJANGO_ENV')
if not DJANGO_ENV:
    DJANGO_ENV = 'development'

SETTINGS_MODULE = f"config.settings.{DJANGO_ENV}"
