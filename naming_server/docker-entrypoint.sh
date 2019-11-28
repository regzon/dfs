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

exec $@
