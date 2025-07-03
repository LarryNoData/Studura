#!/bin/bash
echo "Starting Studura at $(date)"

set -e  # Exit immediately if any command fails

# Run migration and capture errors
if flask db upgrade; then
    echo "Migration complete"
else
    echo "Migration failed"
    exit 1
fi


# Start the Gunicorn server
exec gunicorn app:app
