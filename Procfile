release: python manage.py migrate
web: gunicorn AllyBackend.asgi:application -b 0.0.0.0:$PORT -w 4 -k uvicorn.workers.UvicornWorker
celeryworker:  celery -A AllyBackend worker -l info -B --autoscale=6,3