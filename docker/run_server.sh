#!/usr/bin/env bash

echo "Starting server"

uvicorn main:app --host 0.0.0.0 --port 80


exec "$@"
