#!/bin/bash
export DJANGO_SETTINGS_MODULE=core.settings

python manage.py makemigrations 
python manage.py migrate 
python manage.py createsuperuser --no-input
# python manage.py collectstatic --no-input
# python manage.py runserver 0.0.0.0:8000
# gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
gunicorn --reload --config gunicorn-cfg.py core.wsgi -b 0.0.0.0:8000

