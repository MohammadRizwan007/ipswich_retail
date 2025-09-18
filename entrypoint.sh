#!/bin/sh

set -e

# Wait for the database to be ready
until python manage.py check --database default; do
  >&2 echo "Database is unavailable - sleeping"
  sleep 1
done

>&2 echo "Database is up - continuing"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 3