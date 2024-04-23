#!/bin/bash
export DJANGO_SETTINGS_MODULE=core.settings

# wait for Postgres to start
until python manage.py makemigrations; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done

echo >&2 "Postgres is up - continuing"

python manage.py makemigrations 
python manage.py migrate 
python manage.py createsuperuser --no-input
python manage.py collectstatic --no-input
# python manage.py runserver 0.0.0.0:8000
# gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
# #switch to asgi
gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker --reload --config gunicorn-cfg.py -b 0.0.0.0:8000


