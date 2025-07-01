#!/bin/bash
set -e              # fail fast on any error
flask db upgrade    # apply migrations on Render
exec gunicorn app:app
