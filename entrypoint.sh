#!/bin/sh

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 pitstop.wsgi:application
