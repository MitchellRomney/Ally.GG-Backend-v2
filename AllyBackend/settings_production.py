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
    'https://ally.gg',
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

sentry_sdk.init(
    dsn="https://ee789799be9c4c3ab7411232f46b164c@sentry.io/1444367",
    integrations=[DjangoIntegration(), CeleryIntegration()],
    send_default_pii=True,
    environment='API (Production)'
)
