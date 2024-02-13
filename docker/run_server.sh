#!/usr/bin/env bash

echo "Starting server"

uvicorn main:app --host 0.0.0.0 --port 80 &

sleep 10

echo "Starting celery"

celery -A price_updater.celery_worker.celery beat --loglevel=info --logfile=price_updater/celery.log &

sleep 10

celery -A price_updater.celery_worker.celery worker

exec "$@"
