#!/bin/bash
echo "Starting Studura at $(date)"

set -e  # Exit immediately if any command fails


python manage.py db stamp 3f9c2a1b7e4a


# Run migration and capture errors
if ! python manage.py db upgrade; then
    echo "DB upgrade failed"
    exit 1
else
    echo "Database upgraded succesfully"
fi

# Start the Gunicorn server
exec gunicorn app:app
