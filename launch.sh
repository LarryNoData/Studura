#!/bin/bash
echo "Starting Studura at $(date -u)"

set -e  # Exit immediately if any command fails

# Stamp the database to the latest migration revision
until python manage.py db stamp head; do
    echo "Waiting for DB to be available..."
    sleep 5
done


# Run migration and capture errors
if ! python manage.py db upgrade; then
    echo "DB upgrade failed"
    exit 1
else
    echo "Database upgraded successfully"
fi

# Start the Gunicorn server
exec gunicorn app:app