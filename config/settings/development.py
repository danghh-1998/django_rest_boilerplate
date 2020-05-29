from .base import *
from environ import Env

SECRET_KEY = 'manh5ag9_tgp$l7du6e)mm_+iqr$t-u7rb!9#n6^!hja(&dx1$'
ENV_PATH = os.path.join(BASE_DIR, '.env')

env = Env()
if os.path.exists(ENV_PATH):
    env.read_env(ENV_PATH)

TOKEN_EXPIRED_AFTER_SECONDS = env.int('TOKEN_EXPIRED_AFTER_SECONDS')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
SENDGRID_API_KEY = env('SENDGRID_API_KEY')

DEBUG = True
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )
CORS_ORIGIN_ALLOW_ALL = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0'
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
