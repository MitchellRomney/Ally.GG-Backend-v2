import dj_database_url
from AllyBackend.settings import *

RIOT_API_KEY = os.environ.get('RIOT_API_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = [
    'admin.ally.gg',
    'api.ally.gg',
    'ally-gg-backend.herokuapp.com'
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'https://www.ally.gg',
    'http://www.ally.gg',
    'https://ally.gg',
    'http://ally.gg',
]

DEBUG = False

DEVELOPER_MODE = False

SECURE_SSL_REDIRECT = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'support@ally.gg'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587
