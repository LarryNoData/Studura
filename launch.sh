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

if ! python python manage.py db stamp 0c14b2722228; then
    echo "DB stamp failed"
    exit 1
else
    echo "Database stamped succesfully"
fi

# Run migration and capture errors
if ! python manage.py db upgrade; then
    echo "DB upgrade failed"
    exit 1
else
    echo "Database upgraded succesfully"
fi

# Start the Gunicorn server
exec gunicorn app:app
