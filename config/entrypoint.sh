#!/bin/bash

source venv/bin/activate
RUN_PORT="8000"

echo "Waiting for postgres..."

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while true; do
      python3 manage.py showmigrations
      if [[ "$?" == "0" ]]; then
        break
      fi
      sleep 10
    done

    echo "PostgreSQL started"
fi


venv/bin/python manage.py flush --no-input
venv/bin/python manage.py migrate --no-input
venv/bin/gunicorn --bind "0.0.0.0:${RUN_PORT}" --access-logfile - --error-logfile - config.wsgi:application
