#!/bin/sh

echo 'Waiting for PostgreSQL to be ready...'
while ! nc -z cinema_db 5432; do
  sleep 0.5
done

echo 'Starting FastAPI...'
exec uvicorn app.main:app --host 0.0.0.0 --port 8000