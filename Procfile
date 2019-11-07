release: python manage.py migrate
web: daphne AllyBackend.asgi:application --port $PORT --bind 0.0.0.0 -v2
celeryworker:  celery -A AllyBackend worker -l info -B --autoscale=6,3