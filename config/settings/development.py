from .base import *
from environ import Env

SECRET_KEY = 'manh5ag9_tgp$l7du6e)mm_+iqr$t-u7rb!9#n6^!hja(&dx1$'
ENV_PATH = os.path.join(BASE_DIR, '.env')

env = Env()
if os.path.exists(ENV_PATH):
    env.read_env(ENV_PATH)

DEBUG = True
INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': env('DB_HOST'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'NAME': env('DB_NAME')
    }
}

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
