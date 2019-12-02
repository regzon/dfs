#!/usr/bin/env bash

set -ex

echo "Making database migrations..."
python manage.py makemigrations
echo "Done"
echo

echo "Migrating the database..."
python manage.py migrate
echo "Done"
echo

# Run the application
if [ "$1" = 'uwsgi' ]; then
  echo "Starting uwsgi..."
  exec $@ \
    --master \
    --module=naming_server.wsgi \
    --spooler=/spools \
    --spooler-frequency=10 \
    --processes=$UWSGI_PROCESSES \
    --threads=$UWSGI_THREADS \
    --http-socket=0.0.0.0:80
fi

exec $@
