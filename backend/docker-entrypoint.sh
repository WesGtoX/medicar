#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000
