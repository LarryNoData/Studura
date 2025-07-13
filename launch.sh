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
if ! python python manage.py db stamp f6e5d4c3b2a1; then
    echo "DB stamp failed"
    exit 1
else
    echo "Database stamped successfully to f6e5d4c3b2a1"
fi

# Start the Gunicorn server
exec gunicorn app:app
