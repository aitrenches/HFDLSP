#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
    done

    echo "Postgres database has initialized successfully"
fi

exec "$@"