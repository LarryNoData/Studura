#!/bin/bash
echo "Starting Studura at $(date -u)"

set -e  # Exit immediately if any command fails

# Stamp the database to the latest migration revision
python manage.py db stamp 3f9c2a1b7e4a || {
    echo "DB stamp failed"
    exit 1
}

# Run migration and capture errors
if ! python manage.py db upgrade; then
    echo "DB upgrade failed"
    exit 1
else
    echo "Database upgraded successfully"
fi

# Start the Gunicorn server
exec gunicorn app:app