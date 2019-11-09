release: python manage.py migrate
web: uvicorn AllyBackend.asgi:application --port $PORT
celeryworker:  celery -A AllyBackend worker -l info -B --autoscale=6,3