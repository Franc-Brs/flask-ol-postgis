#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$IS_FLASK" = "True" ] ; then
    flask db migrate
    flask db upgrade

    python manage.py run -h 0.0.0.0
else
  celery -A manage.celery worker --loglevel=info
fi


exec "$@"