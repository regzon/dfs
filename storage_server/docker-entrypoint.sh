#!/usr/bin/env bash

set -ex

# Generate storage id
if [ ! -f /var/application/id ]; then
    python -c "import uuid; print(uuid.uuid4())" > /var/application/id
fi
export STORAGE_ID=$(cat /var/application/id)

# Run the application
if [ "$1" = 'uwsgi' ]; then
  echo "Starting uwsgi..."
  exec $@ \
    --master \
    --module=application.wsgi \
    --spooler=/spools \
    --spooler-frequency=10 \
    --import=application.tasks \
    --processes=$UWSGI_PROCESSES \
    --threads=$UWSGI_THREADS \
    --http-socket=0.0.0.0:5000
fi

exec $@
