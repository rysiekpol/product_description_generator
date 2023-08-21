#!/bin/bash

echo "Running Python version: $(which python)"
RUN_PORT="$PORT"

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while true; do
      python manage.py showmigrations
      if [[ "$?" == "0" ]]; then
        break
      fi
      sleep 3
    done

    echo "PostgreSQL started"
fi


set -e # exit if errors happen anywhere
python manage.py collectstatic --no-input --clear
python manage.py makemigrations
python manage.py migrate --no-input
gunicorn --bind "0.0.0.0:5001" --access-logfile - --error-logfile - config.wsgi:application