from .base import *

DEBUG = False

SECRET_KEY = 'azyr8U@S9GqFwdY79t^Edlwb#Q@7'
TOKEN_EXPIRED_AFTER_SECONDS = 86400

EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'secret_password'
DEFAULT_FROM_EMAIL = 'example@gmail.com'
VERIFY_EMAIL_TOKEN_EXPIRED_AFTER = 86400

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
