#!/usr/bin/env bash

echo "Starting"

alembic upgrade head

echo "migrations done"

exec "$@"
