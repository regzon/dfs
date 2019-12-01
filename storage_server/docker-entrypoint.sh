#!/usr/bin/env bash

set -ex

if [ "$1" = 'uwsgi' ]; then
  echo "Starting uwsgi..."
  exec $@ \
    --master \
    --module=application.wsgi \
    --spooler=/spools \
    --import=application.tasks \
    --processes=$UWSGI_PROCESSES \
    --threads=$UWSGI_THREADS \
    --http-socket=0.0.0.0:5000
fi

exec $@
