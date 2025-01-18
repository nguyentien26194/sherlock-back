#!/bin/bash

set -e

cd /app

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

echo "Waiting for Postgres..."
until postgres_ready; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "Postgres is up - continuing..."

echo "Running migrations..."

PYTHONBUFFERED=1 python sherlock/manage.py migrate

echo "Running tests..."
PYTHONBUFFERED=1 python sherlock/manage.py test -v 2 sherlock/
