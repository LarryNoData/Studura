#!/bin/bash
echo "Starting Studura at $(date)"

set -e  # Exit immediately if any command fails

# Run migration and capture errors
#if flask db upgrade; then
    #echo "Migration complete"
#else
    #echo "Migration failed"
    #exit 1
#fi

# Run migration and capture errors
if ! python manage.py db upgrade; then
    echo "DB upgrade failed"
    exit 1
else
    echo "Database upgraded successfully"
fi

# Start the Gunicorn server
exec gunicorn app:app
