from .base import *

DEBUG = False

SECRET_KEY = 'azyr8U@S9GqFwdY79t^Edlwb#Q@7'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql',
        'USER': 'root',
        'PASSWORD': '12345678',
        'NAME': 'ci_test'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
