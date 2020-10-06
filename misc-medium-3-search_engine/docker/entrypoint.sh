#!/bin/sh
echo 'Waiting for PostgreSQL to start...'

while ! nc -z "misc-6-medium-db" "5432"; do
	sleep 0.2
done

echo 'PostgreSQL started!'

sleep 1

exec "$@"
