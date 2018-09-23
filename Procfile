web: gunicorn --log-level=${LOG_LEVEL} hubble.wsgi
worker: celery -A hubble.tasks worker --loglevel=info
